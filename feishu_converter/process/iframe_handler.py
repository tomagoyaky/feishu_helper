"""
内嵌 Block 处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class IFrameHandler(BaseHandler):
    """
    处理内嵌 Block 类型的块
    """
    
    @staticmethod
    def process_iframe(iframe_block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理内嵌 Block 块
        
        :param iframe_block: 内嵌 Block 块
        :param markdown_lines: Markdown行列表
        """
        # 暂时不做具体处理
        pass