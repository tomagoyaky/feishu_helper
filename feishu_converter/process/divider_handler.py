"""
分割线处理器类
"""
from typing import List
from .base_handler import BaseHandler


class DividerHandler(BaseHandler):
    """
    处理分割线类型的块
    """
    
    @staticmethod
    def process_divider(markdown_lines: List[str]):
        """
        处理分割线
        
        :param markdown_lines: Markdown行列表
        """
        markdown_lines.append("---")
        DividerHandler.add_empty_line(markdown_lines)