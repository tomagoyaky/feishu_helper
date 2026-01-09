"""
任务处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class TaskHandler(BaseHandler):
    """
    处理任务类型的块
    """
    
    @staticmethod
    def process_task(block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理任务块
        
        :param block: 块数据
        :param markdown_lines: Markdown行列表
        """
        markdown_lines.append("<!-- 任务块 -->")
        TaskHandler.add_empty_line(markdown_lines)