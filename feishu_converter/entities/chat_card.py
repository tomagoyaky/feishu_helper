"""
会话卡片块实体定义
"""
from typing import List, Optional
from dataclasses import dataclass
from ..enums import Align


@dataclass
class ChatCard:
    """
    会话卡片块的内容实体
    """
    chat_id: str
    align: Optional[Align] = None