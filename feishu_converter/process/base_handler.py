"""
基础处理器类
"""
from typing import Dict, Any, List


class BaseHandler:
    """
    所有处理器的基础类
    """
    
    @staticmethod
    def extract_text_with_style(element: Dict[str, Any]) -> str:
        """
        从元素中提取带样式的文本
        
        :param element: 元素数据
        :return: 带样式的文本
        """
        if 'text_run' in element:
            text_run = element['text_run']
            content = text_run.get('content', '')
            
            # 处理文本样式
            style = text_run.get('text_element_style', {})
            if style:
                bold = style.get('bold', False)
                italic = style.get('italic', False)
                strikethrough = style.get('strikethrough', False)
                inline_code = style.get('inline_code', False)
                
                if bold:
                    content = f"**{content}**"
                if italic:
                    content = f"*{content}*"
                if strikethrough:
                    content = f"~~{content}~~"
                if inline_code:
                    content = f"`{content}`"
            
            return content
        
        return ""
    
    @staticmethod
    def add_empty_line(markdown_lines: List[str]):
        """
        向markdown行列表添加空行
        
        :param markdown_lines: Markdown行列表
        """
        if markdown_lines and markdown_lines[-1] != "":
            markdown_lines.append("")