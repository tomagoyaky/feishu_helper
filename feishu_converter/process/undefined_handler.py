"""
未定义处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class UndefinedHandler(BaseHandler):
    """
    处理未定义类型的块
    """
    
    @staticmethod
    def process_undefined(undefined_block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理未定义块
        
        :param undefined_block: 未定义块
        :param markdown_lines: Markdown行列表
        """
        # 暂时不做具体处理
        pass