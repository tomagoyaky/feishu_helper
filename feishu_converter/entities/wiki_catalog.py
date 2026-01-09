"""
Wiki目录块实体定义
"""
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class WikiCatalog:
    """
    Wiki 子目录块的内容实体
    """
    wiki_token: Optional[str] = None