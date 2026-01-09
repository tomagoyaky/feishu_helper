"""
源同步块实体定义
"""
from typing import List, Optional
from dataclasses import dataclass
from ..enums import Align
from .text_elements import TextElement


@dataclass
class SourceSynced:
    """
    源同步块的内容实体
    """
    elements: Optional[List[TextElement]] = None
    align: Optional[Align] = None