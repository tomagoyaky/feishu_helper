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
        markdown_lines.append("<!-- 分栏布局开始 -->")
        markdown_lines.append("### 分栏布局")
        
        # 处理分栏内容
        if 'grid' in grid_block:
            grid_data = grid_block['grid']
            
            # 提取列信息
            if 'columns' in grid_data:
                columns = grid_data['columns']
                if columns:
                    for i, column in enumerate(columns, 1):
                        markdown_lines.append(f"\n#### 列 {i}")
                        # 列内容通常包含子块，这里简化处理
                        markdown_lines.append("[列内容] - 包含文本、图片等元素")
        else:
            markdown_lines.append("<!-- 分栏块 -->")
        
        markdown_lines.append("<!-- 分栏布局结束 -->")
        GridHandler.add_empty_line(markdown_lines)