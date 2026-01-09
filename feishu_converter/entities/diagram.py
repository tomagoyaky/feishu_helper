"""
流程图 & UML 图块实体定义
"""
from typing import List, Optional
from dataclasses import dataclass
from ..enums import DiagramType


@dataclass
class Diagram:
    """
    流程图 & UML 图块的内容实体
    """
    diagram_type: Optional[DiagramType] = None