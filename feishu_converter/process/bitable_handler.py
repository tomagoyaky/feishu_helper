"""
多维表格处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class BitableHandler(BaseHandler):
    """
    处理多维表格类型的块
    """
    
    @staticmethod
    def process_bitable(bitable_block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理多维表格块
        
        :param bitable_block: 多维表格块
        :param markdown_lines: Markdown行列表
        """
        # 暂时不做具体处理
        pass