"""
文件块实体定义
"""
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class File:
    """
    文件块的内容实体
    """
    token: Optional[str] = None
    name: Optional[str] = None
    view_type: Optional[int] = None  # 1: 卡片视图（默认）, 2: 预览视图