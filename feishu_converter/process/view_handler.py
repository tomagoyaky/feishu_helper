"""
视图处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class ViewHandler(BaseHandler):
    """
    处理视图类型的块
    """
    
    @staticmethod
    def process_view(block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理视图块
        
        :param block: 块数据
        :param markdown_lines: Markdown行列表
        """
        markdown_lines.append("<!-- 视图块 -->")
        ViewHandler.add_empty_line(markdown_lines)