"""
思维笔记处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class MindNoteHandler(BaseHandler):
    """
    处理思维笔记类型的块
    """
    
    @staticmethod
    def process_mind_note(mind_note_block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理思维笔记块
        
        :param mind_note_block: 思维笔记块
        :param markdown_lines: Markdown行列表
        """
        # 暂时不做具体处理
        pass