"""
引用处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class QuoteHandler(BaseHandler):
    """
    处理引用相关的块类型
    """
    
    @staticmethod
    def process_quote(block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理引用块
        
        :param block: 块数据
        :param markdown_lines: Markdown行列表
        """
        elements = block.get('quote', {}).get('elements', [])
        text_parts = []
        
        for element in elements:
            content = QuoteHandler.extract_text_with_style(element)
            if content:
                text_parts.append(content)
        
        if text_parts:
            quoted_lines = ['> ' + line for line in ''.join(text_parts).split('\n')]
            markdown_lines.extend(quoted_lines)
            QuoteHandler.add_empty_line(markdown_lines)