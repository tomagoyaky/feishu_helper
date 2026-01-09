"""
链接预览处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class LinkPreviewHandler(BaseHandler):
    """
    处理链接预览类型的块
    """
    
    @staticmethod
    def process_link_preview(block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理链接预览块
        
        :param block: 块数据
        :param markdown_lines: Markdown行列表
        """
        markdown_lines.append("<!-- 链接预览块 -->")
        LinkPreviewHandler.add_empty_line(markdown_lines)