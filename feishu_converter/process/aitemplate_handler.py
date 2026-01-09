"""
AI模板处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class AitemplateHandler(BaseHandler):
    """
    处理AI模板类型的块
    """
    
    @staticmethod
    def process_aitemplate(block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理AI模板块
        
        :param block: 块数据
        :param markdown_lines: Markdown行列表
        """
        markdown_lines.append("<!-- AI模板块 -->")
        AitemplateHandler.add_empty_line(markdown_lines)