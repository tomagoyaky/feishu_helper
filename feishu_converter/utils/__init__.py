"""
工具函数模块
包含常用的工具函数
"""

import re
from urllib.parse import urlparse

# 导出新的工具类
from .image_utils import ImageUtils, ImageCacheManager
from .retry_utils import (
    RetryConfig,
    retry_with_backoff,
    retry_on_rate_limit,
    CircuitBreaker,
    CircuitBreakerOpenError,
    FallbackStrategy,
    with_fallback,
    RequestSessionManager,
    safe_request,
    safe_get,
    safe_post
)


def validate_url(url: str) -> bool:
    """
    验证URL是否有效
    
    :param url: 待验证的URL
    :return: 是否有效
    """
    # 支持的飞书文档链接格式
    # - https://xxx.feishu.cn/docx/{doc_id}
    # - https://xxx.feishu.cn/docs/{doc_id}
    # - https://xxx.feishu.cn/wiki/{doc_id}
    
    feishu_pattern = re.compile(
        r'^https://[a-zA-Z0-9.-]+\.feishu\.cn/(docx|docs|wiki)/[a-zA-Z0-9_-]+',
        re.IGNORECASE
    )
    
    return bool(feishu_pattern.match(url))


def extract_doc_id_from_url(url: str) -> str:
    """
    从URL中提取文档ID
    
    :param url: 飞书文档链接
    :return: 文档ID
    """
    parsed = urlparse(url)
    if 'feishu.cn' in parsed.netloc:
        # 飞书文档链接格式: https://xxx.feishu.cn/docx/{doc_id}
        # 飞书旧版文档链接格式: https://xxx.feishu.cn/docs/{doc_id}
        # 飞书wiki链接格式: https://xxx.feishu.cn/wiki/{doc_id}
        path_parts = parsed.path.strip('/').split('/')
        if len(path_parts) >= 2 and path_parts[0] in ['docx', 'docs', 'wiki']:
            return path_parts[1]
    
    return None


__all__ = [
    # URL工具
    'validate_url',
    'extract_doc_id_from_url',
    # 图片工具
    'ImageUtils',
    'ImageCacheManager',
    # 重试工具
    'RetryConfig',
    'retry_with_backoff',
    'retry_on_rate_limit',
    'CircuitBreaker',
    'CircuitBreakerOpenError',
    'FallbackStrategy',
    'with_fallback',
    'RequestSessionManager',
    'safe_request',
    'safe_get',
    'safe_post',
]
