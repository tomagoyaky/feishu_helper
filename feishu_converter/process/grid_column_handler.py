"""
分栏列处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class GridColumnHandler(BaseHandler):
    """
    处理分栏列类型的块
    """
    
    @staticmethod
    def process_grid_column(grid_column_block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理分栏列块
        
        :param grid_column_block: 分栏列块
        :param markdown_lines: Markdown行列表
        """
        # 暂时不做具体处理
        pass