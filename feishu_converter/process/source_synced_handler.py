"""
源同步块处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class SourceSyncedHandler(BaseHandler):
    """
    处理源同步块类型的块
    """
    
    @staticmethod
    def process_source_synced(source_synced_block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理源同步块
        
        :param source_synced_block: 源同步块
        :param markdown_lines: Markdown行列表
        """
        # 暂时不做具体处理
        pass