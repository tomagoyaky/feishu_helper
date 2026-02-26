"""
重试机制和错误恢复工具
提供装饰器和工具函数用于处理网络请求的重试和错误恢复
"""

import functools
import logging
import random
import time
from typing import Callable, Optional, Tuple, Type, Union

import requests


class RetryConfig:
    """重试配置类"""

    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        retry_exceptions: Tuple[Type[Exception], ...] = None,
        retry_status_codes: Tuple[int, ...] = None,
        on_retry: Optional[Callable] = None,
        on_failure: Optional[Callable] = None
    ):
        """
        初始化重试配置

        :param max_retries: 最大重试次数
        :param base_delay: 基础延迟时间（秒）
        :param max_delay: 最大延迟时间（秒）
        :param exponential_base: 指数退避基数
        :param retry_exceptions: 需要重试的异常类型
        :param retry_status_codes: 需要重试的HTTP状态码
        :param on_retry: 重试时的回调函数
        :param on_failure: 最终失败时的回调函数
        """
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.retry_exceptions = retry_exceptions or (requests.exceptions.RequestException,)
        self.retry_status_codes = retry_status_codes or (429, 500, 502, 503, 504)
        self.on_retry = on_retry
        self.on_failure = on_failure


def retry_with_backoff(config: Optional[RetryConfig] = None):
    """
    重试装饰器，使用指数退避策略

    :param config: 重试配置
    :return: 装饰器函数
    """
    if config is None:
        config = RetryConfig()

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(func.__module__)
            last_exception = None

            for attempt in range(config.max_retries + 1):
                try:
                    return func(*args, **kwargs)

                except config.retry_exceptions as e:
                    last_exception = e

                    # 检查是否需要重试
                    should_retry = True

                    # 如果是HTTP错误，检查状态码
                    if hasattr(e, 'response') and e.response is not None:
                        status_code = e.response.status_code
                        if status_code not in config.retry_status_codes:
                            should_retry = False
                            logger.warning(f"HTTP {status_code} 错误，不重试: {e}")

                    if not should_retry:
                        raise

                    # 如果是最后一次尝试，不再重试
                    if attempt >= config.max_retries:
                        logger.error(f"函数 {func.__name__} 在 {config.max_retries} 次重试后仍然失败")
                        if config.on_failure:
                            config.on_failure(e, attempt)
                        raise

                    # 计算延迟时间（指数退避 + 随机抖动）
                    delay = min(
                        config.base_delay * (config.exponential_base ** attempt),
                        config.max_delay
                    )
                    # 添加随机抖动（±20%）
                    jitter = delay * 0.2 * (2 * random.random() - 1)
                    actual_delay = delay + jitter

                    logger.warning(
                        f"函数 {func.__name__} 第 {attempt + 1} 次尝试失败: {e}. "
                        f"{actual_delay:.2f}秒后重试..."
                    )

                    if config.on_retry:
                        config.on_retry(e, attempt, actual_delay)

                    time.sleep(actual_delay)

            # 如果所有重试都失败
            if last_exception:
                raise last_exception

        return wrapper
    return decorator


def retry_on_rate_limit(max_retries: int = 3, base_delay: float = 2.0):
    """
    专门用于处理速率限制的重试装饰器

    :param max_retries: 最大重试次数
    :param base_delay: 基础延迟时间
    :return: 装饰器函数
    """
    config = RetryConfig(
        max_retries=max_retries,
        base_delay=base_delay,
        retry_status_codes=(429,),
        retry_exceptions=(requests.exceptions.HTTPError,)
    )
    return retry_with_backoff(config)


class CircuitBreaker:
    """
    熔断器模式实现
    用于防止连续失败请求对系统造成过大压力
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        expected_exception: Type[Exception] = Exception
    ):
        """
        初始化熔断器

        :param failure_threshold: 失败次数阈值
        :param recovery_timeout: 恢复超时时间（秒）
        :param expected_exception: 预期的异常类型
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception

        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
        self.logger = logging.getLogger(__name__)

    def can_execute(self) -> bool:
        """检查是否可以执行"""
        if self.state == 'CLOSED':
            return True

        if self.state == 'OPEN':
            if time.time() - self.last_failure_time >= self.recovery_timeout:
                self.state = 'HALF_OPEN'
                self.logger.info("熔断器进入半开状态，允许测试请求")
                return True
            return False

        return True  # HALF_OPEN

    def record_success(self):
        """记录成功"""
        self.failure_count = 0
        if self.state == 'HALF_OPEN':
            self.state = 'CLOSED'
            self.logger.info("熔断器关闭，服务恢复正常")

    def record_failure(self):
        """记录失败"""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = 'OPEN'
            self.logger.warning(f"熔断器打开，连续失败 {self.failure_count} 次")

    def __call__(self, func: Callable) -> Callable:
        """装饰器实现"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not self.can_execute():
                raise CircuitBreakerOpenError("熔断器打开，请求被拒绝")

            try:
                result = func(*args, **kwargs)
                self.record_success()
                return result
            except self.expected_exception as e:
                self.record_failure()
                raise

        return wrapper


class CircuitBreakerOpenError(Exception):
    """熔断器打开错误"""
    pass


class FallbackStrategy:
    """降级策略"""

    @staticmethod
    def return_none(*args, **kwargs):
        """返回None"""
        return None

    @staticmethod
    def return_empty_dict(*args, **kwargs):
        """返回空字典"""
        return {}

    @staticmethod
    def return_empty_list(*args, **kwargs):
        """返回空列表"""
        return []

    @staticmethod
    def return_default(default_value):
        """返回默认值"""
        def fallback(*args, **kwargs):
            return default_value
        return fallback

    @staticmethod
    def raise_custom_error(message: str):
        """抛出自定义错误"""
        def fallback(*args, **kwargs):
            raise RuntimeError(message)
        return fallback


def with_fallback(fallback_func: Callable = None):
    """
    降级装饰器
    当主函数失败时，执行降级函数

    :param fallback_func: 降级函数
    :return: 装饰器
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger = logging.getLogger(func.__module__)
                logger.warning(f"函数 {func.__name__} 失败，执行降级策略: {e}")

                if fallback_func:
                    return fallback_func(*args, **kwargs)
                raise

        return wrapper
    return decorator


class RequestSessionManager:
    """请求会话管理器"""

    def __init__(
        self,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
        status_forcelist: Tuple[int, ...] = (500, 502, 503, 504),
        timeout: float = 30.0
    ):
        """
        初始化会话管理器

        :param max_retries: 最大重试次数
        :param backoff_factor: 退避因子
        :param status_forcelist: 需要重试的状态码
        :param timeout: 超时时间
        """
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.status_forcelist = status_forcelist
        self.timeout = timeout
        self._session = None

    def get_session(self) -> requests.Session:
        """获取配置好的会话"""
        if self._session is None:
            self._session = requests.Session()

            # 配置重试策略
            from requests.adapters import HTTPAdapter
            from urllib3.util.retry import Retry

            retry_strategy = Retry(
                total=self.max_retries,
                backoff_factor=self.backoff_factor,
                status_forcelist=self.status_forcelist,
                allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE", "PATCH"]
            )

            adapter = HTTPAdapter(max_retries=retry_strategy)
            self._session.mount("http://", adapter)
            self._session.mount("https://", adapter)

        return self._session

    def close(self):
        """关闭会话"""
        if self._session:
            self._session.close()
            self._session = None

    def __enter__(self):
        return self.get_session()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# 便捷函数

def safe_request(
    method: str,
    url: str,
    max_retries: int = 3,
    timeout: float = 30.0,
    **kwargs
) -> requests.Response:
    """
    安全的HTTP请求函数，带重试机制

    :param method: HTTP方法
    :param url: 请求URL
    :param max_retries: 最大重试次数
    :param timeout: 超时时间
    :param kwargs: 其他请求参数
    :return: 响应对象
    """
    logger = logging.getLogger(__name__)

    for attempt in range(max_retries + 1):
        try:
            response = requests.request(method, url, timeout=timeout, **kwargs)
            response.raise_for_status()
            return response

        except requests.exceptions.RequestException as e:
            if attempt >= max_retries:
                logger.error(f"请求 {url} 在 {max_retries} 次重试后仍然失败")
                raise

            delay = min(2 ** attempt, 30)  # 最大30秒
            logger.warning(f"请求失败（尝试 {attempt + 1}/{max_retries + 1}）: {e}，{delay}秒后重试...")
            time.sleep(delay)


def safe_get(url: str, **kwargs) -> requests.Response:
    """安全的GET请求"""
    return safe_request('GET', url, **kwargs)


def safe_post(url: str, **kwargs) -> requests.Response:
    """安全的POST请求"""
    return safe_request('POST', url, **kwargs)
