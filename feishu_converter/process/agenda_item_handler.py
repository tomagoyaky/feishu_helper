"""
议程项处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class AgendaItemHandler(BaseHandler):
    """
    处理议程项类型的块
    """
    
    @staticmethod
    def process_agenda_item(block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理议程项块
        
        :param block: 块数据
        :param markdown_lines: Markdown行列表
        """
        markdown_lines.append("<!-- 议程项块 -->")
        AgendaItemHandler.add_empty_line(markdown_lines)