"""
画板块实体定义
"""
from typing import List, Optional
from dataclasses import dataclass
from ..enums import Align


@dataclass
class Board:
    """
    画板块的内容实体
    """
    token: Optional[str] = None
    align: Optional[Align] = None
    width: Optional[int] = None
    height: Optional[int] = None