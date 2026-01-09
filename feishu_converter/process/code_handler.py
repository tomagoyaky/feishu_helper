"""
代码处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class CodeHandler(BaseHandler):
    """
    处理代码相关的块类型
    """
    
    @staticmethod
    def process_code(block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理代码块
        
        :param block: 块数据
        :param markdown_lines: Markdown行列表
        """
        elements = block.get('code', {}).get('elements', [])
        code_content = ""
        language = block.get('code', {}).get('language', 'text')  # 默认为text
        
        for element in elements:
            if 'text_run' in element:
                content = element['text_run'].get('content', '')
                code_content += content
        
        if code_content:
            markdown_lines.append(f"```{language}")
            markdown_lines.append(code_content)
            markdown_lines.append("```")
            CodeHandler.add_empty_line(markdown_lines)