"""
议程项标题块实体定义
"""
from typing import List, Optional
from dataclasses import dataclass
from ..enums import Align
from .text_elements import AgendaTitleElement


@dataclass
class AgendaItemTitle:
    """
    议程项标题块
    """
    align: Optional[Align] = None
    elements: Optional[List[AgendaTitleElement]] = None