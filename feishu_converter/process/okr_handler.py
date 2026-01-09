"""
OKR处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class OKRHandler(BaseHandler):
    """
    处理OKR类型的块
    """
    
    @staticmethod
    def process_okr(okr_block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理OKR块
        
        :param okr_block: OKR块
        :param markdown_lines: Markdown行列表
        """
        # 暂时不做具体处理
        pass