"""
列表处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class ListHandler(BaseHandler):
    """
    处理列表相关的块类型
    """
    
    @staticmethod
    def process_bullet_list(block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理无序列表块
        
        :param block: 块数据
        :param markdown_lines: Markdown行列表
        """
        elements = block.get('bullet', {}).get('elements', [])
        text_parts = []
        
        for element in elements:
            content = ListHandler.extract_text_with_style(element)
            if content:
                text_parts.append(content)
        
        if text_parts:
            markdown_lines.append(f"- {''.join(text_parts)}")
            ListHandler.add_empty_line(markdown_lines)
    
    @staticmethod
    def process_ordered_list(block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理有序列表块
        
        :param block: 块数据
        :param markdown_lines: Markdown行列表
        """
        elements = block.get('ordered', {}).get('elements', [])
        text_parts = []
        
        for element in elements:
            content = ListHandler.extract_text_with_style(element)
            if content:
                text_parts.append(content)
        
        # 获取列表项的序号，如果没有则默认为1
        sequence = block.get('ordered', {}).get('sequence', 1)
        try:
            index = int(sequence)
        except (ValueError, TypeError):
            index = 1
            
        if text_parts:
            markdown_lines.append(f"{index}. {''.join(text_parts)}")
            ListHandler.add_empty_line(markdown_lines)