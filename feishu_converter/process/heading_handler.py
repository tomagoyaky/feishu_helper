"""
标题处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class HeadingHandler(BaseHandler):
    """
    处理标题相关的块类型
    """
    
    @staticmethod
    def process_heading(block: Dict[str, Any], level: int, markdown_lines: List[str]):
        """
        处理标题块
        
        :param block: 块数据
        :param level: 标题级别
        :param markdown_lines: Markdown行列表
        """
        # 确定使用哪个键来获取元素
        block_key_map = {
            3: 'heading1', 4: 'heading2', 5: 'heading3', 6: 'heading4',
            7: 'heading5', 8: 'heading6', 9: 'heading7', 10: 'heading8', 11: 'heading9'
        }
        
        block_key = block_key_map.get(level + 2, f"heading{level-1}")
        
        if block_key in block:
            elements = block[block_key].get('elements', [])
            text_parts = []
            
            for element in elements:
                content = HeadingHandler.extract_text_with_style(element)
                if content:
                    text_parts.append(content)
            
            if text_parts:
                markdown_lines.append(f"{'#' * level} {''.join(text_parts)}")
                HeadingHandler.add_empty_line(markdown_lines)
    
    @staticmethod
    def process_page(block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理页面块
        
        :param block: 块数据
        :param markdown_lines: Markdown行列表
        """
        elements = block.get('page', {}).get('elements', [])
        for element in elements:
            if 'text_run' in element:
                content = element['text_run']['content']
                markdown_lines.append(f"# {content}")
                HeadingHandler.add_empty_line(markdown_lines)