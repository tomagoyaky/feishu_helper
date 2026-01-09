"""
画板处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class BoardHandler(BaseHandler):
    """
    处理画板类型的块
    """
    
    @staticmethod
    def process_board(block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理画板块
        
        :param block: 块数据
        :param markdown_lines: Markdown行列表
        """
        markdown_lines.append("<!-- 画板块 -->")
        BoardHandler.add_empty_line(markdown_lines)