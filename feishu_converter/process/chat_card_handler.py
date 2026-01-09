"""
会话卡片处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class ChatCardHandler(BaseHandler):
    """
    处理会话卡片类型的块
    """
    
    @staticmethod
    def process_chat_card(chat_card_block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理会话卡片块
        
        :param chat_card_block: 会话卡片块
        :param markdown_lines: Markdown行列表
        """
        # 暂时不做具体处理
        pass