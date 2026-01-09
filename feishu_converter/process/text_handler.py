"""
文本处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class TextHandler(BaseHandler):
    """
    处理各种文本相关的块类型
    """
    
    @staticmethod
    def process_text(block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理文本块
        
        :param block: 块数据
        :param markdown_lines: Markdown行列表
        """
        elements = block.get('text', {}).get('elements', [])
        text_parts = []
        
        for element in elements:
            content = TextHandler.extract_text_with_style(element)
            if content:
                text_parts.append(content)
            elif 'mention_user' in element:
                user_id = element['mention_user'].get('user_id', 'Unknown User')
                text_parts.append(f"@{user_id}")
            elif 'mention_doc' in element:
                doc_title = element['mention_doc'].get('title', 'Unknown Doc')
                url = element['mention_doc'].get('url', '')
                text_parts.append(f"[{doc_title}]({url})")
            elif 'equation' in element:
                equation_content = element['equation'].get('content', '')
                text_parts.append(f"$$ {equation_content} $$")
        
        if text_parts:
            markdown_lines.append(''.join(text_parts))
            TextHandler.add_empty_line(markdown_lines)
    
    @staticmethod
    def process_todo(block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理待办事项块
        
        :param block: 块数据
        :param markdown_lines: Markdown行列表
        """
        elements = block.get('todo', {}).get('elements', [])
        is_done = block.get('todo', {}).get('is_done', False)
        text_parts = []
        
        for element in elements:
            content = TextHandler.extract_text_with_style(element)
            if content:
                text_parts.append(content)
        
        if text_parts:
            status = "x" if is_done else " "
            markdown_lines.append(f"- [{status}] {''.join(text_parts)}")
            TextHandler.add_empty_line(markdown_lines)
    
    @staticmethod
    def process_callout(block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理高亮块
        
        :param block: 块数据
        :param markdown_lines: Markdown行列表
        """
        elements = block.get('callout', {}).get('elements', [])
        text_parts = []
        
        for element in elements:
            content = TextHandler.extract_text_with_style(element)
            if content:
                text_parts.append(content)
        
        if text_parts:
            # 用引用格式表示高亮块
            quoted_lines = ['> ' + line for line in ''.join(text_parts).split('\n')]
            markdown_lines.extend(quoted_lines)
            TextHandler.add_empty_line(markdown_lines)