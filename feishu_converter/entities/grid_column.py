"""
分栏列块实体定义
"""
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class GridColumn:
    """
    分栏列块的内容实体
    """
    width_ratio: Optional[int] = None  # 当前分栏列占整个分栏的比例，取值范围为 [1,99]