"""
分栏处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class GridHandler(BaseHandler):
    """
    处理分栏类型的块
    """
    
    @staticmethod
    def process_grid(grid_block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理分栏块
        
        :param grid_block: 分栏块
        :param markdown_lines: Markdown行列表
        """
        # 暂时不做具体处理
        pass