"""
引用同步块实体定义
"""
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class ReferenceSynced:
    """
    引用同步块的内容实体
    """
    source_block_id: Optional[str] = None
    source_document_id: Optional[str] = None