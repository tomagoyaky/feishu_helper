"""
议程项标题处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class AgendaItemTitleHandler(BaseHandler):
    """
    处理议程项标题类型的块
    """
    
    @staticmethod
    def process_agenda_item_title(agenda_item_title_block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理议程项标题块
        
        :param agenda_item_title_block: 议程项标题块
        :param markdown_lines: Markdown行列表
        """
        # 暂时不做具体处理
        pass