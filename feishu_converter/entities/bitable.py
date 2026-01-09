"""
多维表格块实体定义
"""
from typing import List, Optional
from dataclasses import dataclass
from ..enums import BitableViewType


@dataclass
class Bitable:
    """
    多维表格块的内容实体
    """
    token: str
    view_type: BitableViewType