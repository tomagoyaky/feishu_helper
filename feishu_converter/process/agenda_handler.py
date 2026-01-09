"""
议程处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class AgendaHandler(BaseHandler):
    """
    处理议程类型的块
    """
    
    @staticmethod
    def process_agenda(block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理议程块
        
        :param block: 块数据
        :param markdown_lines: Markdown行列表
        """
        markdown_lines.append("<!-- 议程块 -->")
        AgendaHandler.add_empty_line(markdown_lines)