"""
旧版开放平台小组件块实体定义
"""
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class ISV:
    """
    旧版开放平台小组件块的内容实体
    """
    component_id: Optional[str] = None
    component_type_id: Optional[str] = None