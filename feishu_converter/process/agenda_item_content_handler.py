"""
议程项内容处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class AgendaItemContentHandler(BaseHandler):
    """
    处理议程项内容类型的块
    """
    
    @staticmethod
    def process_agenda_item_content(agenda_item_content_block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理议程项内容块
        
        :param agenda_item_content_block: 议程项内容块
        :param markdown_lines: Markdown行列表
        """
        # 暂时不做具体处理
        pass