"""
Wiki新版子目录块实体定义
"""
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class SubPageList:
    """
    Wiki 新版子目录块的内容实体
    """
    wiki_token: Optional[str] = None