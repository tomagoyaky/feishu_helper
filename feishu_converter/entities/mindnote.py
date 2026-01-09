"""
思维笔记块实体定义
"""
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class Mindnote:
    """
    思维笔记块的内容实体
    """
    token: str