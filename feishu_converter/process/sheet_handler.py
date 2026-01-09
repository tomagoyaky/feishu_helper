"""
电子表格处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class SheetHandler(BaseHandler):
    """
    处理电子表格类型的块
    """
    
    @staticmethod
    def process_sheet(sheet_block: Dict[str, Any], markdown_lines: List[str], spreadsheet_data: Dict[str, Any] = None):
        """
        处理电子表格块，包括潜在的表格数据
        
        :param sheet_block: 电子表格块
        :param markdown_lines: Markdown行列表
        :param spreadsheet_data: 电子表格数据
        """
        # 电子表格通常包含一些元数据，尝试提取相关信息
        sheet_info = sheet_block.get('sheet', {})
        token = sheet_info.get('token')
        
        if token and spreadsheet_data and token in spreadsheet_data:
            # 获取电子表格数据并转换为Markdown表格
            sheet_values = spreadsheet_data[token].get('valueRange', {}).get('values', [])
            
            if sheet_values:
                # 添加电子表格标题
                markdown_lines.append("### 电子表格数据")
                
                # 将电子表格数据转换为Markdown表格
                for i, row in enumerate(sheet_values):
                    # 确保每个单元格都是字符串
                    row_str = []
                    for cell in row:
                        if isinstance(cell, str):
                            row_str.append(cell)
                        elif isinstance(cell, dict):
                            # 如果单元格是字典（如嵌入图像或其他内容），提取文本内容
                            if 'text' in cell:
                                row_str.append(str(cell['text']))
                            elif 'fileToken' in cell:
                                row_str.append("[文件]")
                            else:
                                row_str.append(str(cell))
                        else:
                            row_str.append(str(cell) if cell is not None else "")
                    
                    markdown_lines.append("| " + " | ".join(row_str) + " |")
                    
                    # 如果是第一行，添加分隔行
                    if i == 0:
                        markdown_lines.append("| " + " | ".join(['---'] * len(row_str)) + " |")
                
                SheetHandler.add_empty_line(markdown_lines)  # 添加空行
            else:
                # 如果电子表格中没有数据，显示一个提示
                markdown_lines.append("### 电子表格")
                markdown_lines.append("*此电子表格暂无数据*")
                SheetHandler.add_empty_line(markdown_lines)
        else:
            # 显示电子表格块的基本信息
            title = sheet_info.get('title', '嵌入的电子表格')
            if token:
                base_token = token.split('_')[0] if '_' in token else token  # 获取基础token
                sheet_url = f"https://docs.feiShu.cn/sheets/{base_token}"
                markdown_lines.append(f"**[{title}]({sheet_url})**")
            else:
                markdown_lines.append(f"**{title}**")
            SheetHandler.add_empty_line(markdown_lines)