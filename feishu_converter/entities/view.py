"""
视图块实体定义
"""
from typing import List, Optional
from dataclasses import dataclass
from ..enums import ViewType


@dataclass
class View:
    """
    视图块的内容实体
    """
    view_type: Optional[ViewType] = None