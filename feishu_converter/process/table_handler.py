"""
表格处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class TableHandler(BaseHandler):
    """
    处理表格相关的块类型
    """
    
    @staticmethod
    def process_table(block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理表格块
        
        :param block: 块数据
        :param markdown_lines: Markdown行列表
        """
        table_data = block.get('table', {})
        cells = table_data.get('cells', [])
        property_data = table_data.get('property', {})
        row_size = property_data.get('row_size', 0)
        column_size = property_data.get('column_size', 0)
        
        if row_size > 0 and column_size > 0:
            # 创建表格数据
            table_content = []
            for i in range(row_size):
                row = []
                for j in range(column_size):
                    idx = i * column_size + j
                    if idx < len(cells):
                        # 获取单元格内容
                        cell_data = cells[idx]
                        # 提取文本内容，如果单元格是字典格式
                        if isinstance(cell_data, dict):
                            # 飞书文档中的单元格可能包含复杂内容
                            elements = cell_data.get('table_cell', {}).get('elements', [])
                            cell_text_parts = []
                            for element in elements:
                                content = TableHandler.extract_text_with_style(element)
                                if content:
                                    cell_text_parts.append(content)
                            
                            cell_content = ''.join(cell_text_parts)
                        else:
                            # 如果单元格是简单文本
                            cell_content = str(cell_data) if cell_data else ""
                        
                        row.append(cell_content)
                    else:
                        row.append("")
                table_content.append(row)
            
            # 将表格转换为Markdown格式
            if table_content:
                for i, row in enumerate(table_content):
                    # 将每个单元格内容转义特殊字符（如果需要）
                    formatted_row = [cell.replace('|', '\\|') if cell else '' for cell in row]
                    markdown_lines.append("| " + " | ".join(formatted_row) + " |")
                    
                    # 在第一行后添加分隔行
                    if i == 0:
                        markdown_lines.append("| " + " | ".join(['---'] * len(row)) + " |")
                
                TableHandler.add_empty_line(markdown_lines)