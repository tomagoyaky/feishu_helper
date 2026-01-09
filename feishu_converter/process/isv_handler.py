"""
开放平台小组件处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class ISVHandler(BaseHandler):
    """
    处理开放平台小组件类型的块
    """
    
    @staticmethod
    def process_isv(isv_block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理开放平台小组件块
        
        :param isv_block: 开放平台小组件块
        :param markdown_lines: Markdown行列表
        """
        # 暂时不做具体处理
        pass