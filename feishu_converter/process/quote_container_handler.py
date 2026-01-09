"""
引用容器处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class QuoteContainerHandler(BaseHandler):
    """
    处理引用容器类型的块
    """
    
    @staticmethod
    def process_quote_container(block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理引用容器块
        
        :param block: 块数据
        :param markdown_lines: Markdown行列表
        """
        markdown_lines.append("<!-- 引用容器块 -->")
        QuoteContainerHandler.add_empty_line(markdown_lines)