"""
电子表格块实体定义
"""
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class Sheet:
    """
    电子表格块的内容实体
    """
    token: Optional[str] = None
    row_size: Optional[int] = None
    column_size: Optional[int] = None