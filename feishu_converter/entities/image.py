"""
图片块实体定义
"""
from typing import List, Optional
from dataclasses import dataclass
from ..enums import Align


@dataclass
class Image:
    """
    图片块的内容实体
    """
    token: Optional[str] = None
    width: Optional[int] = 100  # 默认值为100像素
    height: Optional[int] = 100  # 默认值为100像素
    caption: Optional[dict] = None  # {'content': string}
    align: Optional[Align] = None