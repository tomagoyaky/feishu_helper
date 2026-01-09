"""
Wiki目录处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class WikiCatalogHandler(BaseHandler):
    """
    处理Wiki目录类型的块
    """
    
    @staticmethod
    def process_wiki_catalog(block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理Wiki目录块
        
        :param block: 块数据
        :param markdown_lines: Markdown行列表
        """
        markdown_lines.append("<!-- Wiki目录块 -->")
        WikiCatalogHandler.add_empty_line(markdown_lines)