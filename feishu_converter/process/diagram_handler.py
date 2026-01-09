"""
流程图 & UML 处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class DiagramHandler(BaseHandler):
    """
    处理流程图 & UML 类型的块
    """
    
    @staticmethod
    def process_diagram(diagram_block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理流程图 & UML 块
        
        :param diagram_block: 流程图 & UML 块
        :param markdown_lines: Markdown行列表
        """
        # 暂时不做具体处理
        pass