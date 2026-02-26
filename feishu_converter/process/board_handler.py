"""
画板处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class BoardHandler(BaseHandler):
    """
    处理画板类型的块
    """
    
    @staticmethod
    def process_board(block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理画板块
        
        :param block: 块数据
        :param markdown_lines: Markdown行列表
        """
        markdown_lines.append("### 画板")
        
        # 处理画板内容
        if 'board' in block:
            board_data = block['board']
            
            # 提取画板标题
            if 'title' in board_data:
                title = board_data['title']
                if 'content' in title:
                    markdown_lines.append(f"**标题:** {title['content']}")
            
            # 提取画板描述
            if 'description' in board_data:
                description = board_data['description']
                if 'content' in description:
                    markdown_lines.append(f"**描述:** {description['content']}")
            
            # 画板内容通常包含复杂的图形元素，这里使用占位符
            markdown_lines.append("[画板内容] - 包含图形、图表等可视化元素")
        else:
            markdown_lines.append("<!-- 画板块 -->")
        
        BoardHandler.add_empty_line(markdown_lines)