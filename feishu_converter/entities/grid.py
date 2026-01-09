"""
分栏块实体定义
"""
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class Grid:
    """
    分栏块的内容实体
    """
    column_size: int  # 分栏列数量，取值范围为 [2,5]