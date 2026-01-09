"""
内嵌块实体定义
"""
from typing import List, Optional
from dataclasses import dataclass
from ..enums import IframeComponentType


@dataclass
class Iframe:
    """
    内嵌块的内容实体
    """
    component: Optional[dict] = None  # {'type': IframeComponentType, 'url': string}


@dataclass
class IframeComponent:
    """
    Iframe组件
    """
    type: IframeComponentType
    url: str