"""
工具函数
提供一些通用的工具函数
"""

import re


def validate_url(url: str) -> bool:
    """
    验证URL格式是否有效
    
    :param url: 待验证的URL
    :return: 是否有效
    """
    # 飞书文档URL格式: https://xxx.feishu.cn/docx/xxx 或 https://xxx.feishu.cn/docs/xxx
    pattern = r'^https?://[a-zA-Z0-9.-]+\.feishu\.cn/(docx|docs|wiki)/[a-zA-Z0-9_-]+(/.*)?$'
    
    return bool(re.match(pattern, url))