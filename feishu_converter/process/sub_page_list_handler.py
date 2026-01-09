"""
子页面列表处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class SubPageListHandler(BaseHandler):
    """
    处理子页面列表类型的块
    """
    
    @staticmethod
    def process_sub_page_list(block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理子页面列表块
        
        :param block: 块数据
        :param markdown_lines: Markdown行列表
        """
        markdown_lines.append("<!-- 子页面列表块 -->")
        SubPageListHandler.add_empty_line(markdown_lines)