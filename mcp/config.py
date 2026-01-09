"""
飞书助手MCP服务配置文件
"""

import os
from typing import Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv(f'{os.path.join(os.path.dirname(__file__), "..", ".env")}')

# 从环境变量获取配置，如果未设置则使用默认值
APP_ID = os.getenv("APP_ID", "")
APP_SECRET = os.getenv("APP_SECRET", "")
BASE_URL = os.getenv("FEISHU_BASE_URL", "https://open.feishu.cn/open-apis/")
CONVERT_TIMEOUT = int(os.getenv("CONVERT_TIMEOUT", "30"))  # 转换超时时间（秒）

# 日志配置
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "mcp_server.log")

# 缓存配置
CACHE_ENABLED = os.getenv("CACHE_ENABLED", "false").lower() == "true"
CACHE_EXPIRATION = int(os.getenv("CACHE_EXPIRATION", "3600"))  # 缓存过期时间（秒）

def validate_credentials() -> bool:
    """
    验证必要的凭证是否已设置
    :return: 如果凭证有效返回True，否则返回False
    """
    return bool(APP_ID and APP_SECRET)


def get_app_credentials() -> tuple[Optional[str], Optional[str]]:
    """
    获取应用凭证
    :return: (app_id, app_secret) 元组
    """
    return APP_ID or None, APP_SECRET or None