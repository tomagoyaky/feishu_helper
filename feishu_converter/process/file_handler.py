"""
文件处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class FileHandler(BaseHandler):
    """
    处理文件类型的块
    """
    
    @staticmethod
    def process_file(file_block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理文件块
        
        :param file_block: 文件块
        :param markdown_lines: Markdown行列表
        """
        # 暂时不做具体处理
        pass