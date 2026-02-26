"""
电子表格处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler
from ..api import FeishuDocAPI, PermissionType


class SheetHandler(BaseHandler):
    """
    处理电子表格类型的块
    """
    
    @staticmethod
    def process_sheet(sheet_block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理电子表格块，包括潜在的表格数据
        注意：只保留文本内容，不保留样式信息
        
        :param sheet_block: 电子表格块
        :param markdown_lines: Markdown行列表
        """
        # 电子表格通常包含一些元数据，尝试提取相关信息
        sheet_info = sheet_block.get('sheet', {})
        token = sheet_info.get('token')
        
        if token:
            # 分割token以获取电子表格token和工作表ID
            token_parts = token.split('_', 1)  # 只分割一次，得到两部分
            spreadsheet_token = token_parts[0]
            sheet_id = token_parts[1] if len(token_parts) > 1 else None
            
            # 检查是否有权限访问此电子表格
            api = FeishuDocAPI()
            has_permission = api.check_permission(spreadsheet_token, PermissionType.SHEET, "view")
            
            if not has_permission:
                # 如果没有权限，添加引用字符串
                title = sheet_info.get('title', '嵌入的电子表格')
                markdown_lines.append(f"> [{title}](https://docs.feiShu.cn/sheets/{spreadsheet_token}): 需要权限才能访问")
                SheetHandler.add_empty_line(markdown_lines)
                return

            # 获取具体表格数据
            sheet_data = api.get_spreadsheet_data(token)  # 使用原始token，包含电子表格token和工作表ID
            
            if sheet_data:
                # 获取电子表格数据并转换为Markdown表格
                sheet_values = sheet_data.get('valueRange', {}).get('values', [])
                
                if sheet_values:
                    # 添加工作表标题
                    markdown_lines.append(f"### {sheet_info.get('title', '电子表格数据')}")
                    
                    # 将电子表格数据转换为Markdown表格
                    for i, row in enumerate(sheet_values):
                        # 确保每个单元格都是字符串，只保留文本内容
                        row_str = []
                        for cell in row:
                            if isinstance(cell, str):
                                # 直接使用字符串值，不处理样式
                                row_str.append(cell)
                            elif isinstance(cell, dict):
                                # 如果单元格是字典（如嵌入图像或其他内容），提取文本内容
                                if 'text' in cell:
                                    # 只提取文本部分，忽略样式
                                    row_str.append(str(cell['text']))
                                elif 'fileToken' in cell:
                                    row_str.append("[文件]")
                                else:
                                    # 对于其他类型的字典，转换为字符串
                                    row_str.append(str(cell))
                            else:
                                # 对于其他类型，转换为字符串或空字符串
                                row_str.append(str(cell) if cell is not None else "")
                        
                        # 转义表格分隔符，确保Markdown表格格式正确
                        row_str = [cell.replace('|', '\\|') if cell else ' ' for cell in row_str]
                        markdown_lines.append("| " + " | ".join(row_str) + " |")
                        
                        # 如果是第一行，添加分隔行
                        if i == 0:
                            markdown_lines.append("| " + " | ".join(['---'] * len(row_str)) + " |")
                    
                    SheetHandler.add_empty_line(markdown_lines)  # 添加空行
                else:
                    # 如果工作表中没有数据，显示一个提示
                    markdown_lines.append(f"### {sheet_info.get('title', '电子表格')}")
                    markdown_lines.append("*此工作表暂无数据*")
                    SheetHandler.add_empty_line(markdown_lines)
            else:
                # 如果无法获取工作表数据，显示一个链接
                sheet_url = f"https://docs.feiShu.cn/sheets/{spreadsheet_token}"
                title = sheet_info.get('title', '嵌入的电子表格')
                markdown_lines.append(f"**[{title}]({sheet_url})**")
                SheetHandler.add_empty_line(markdown_lines)
        else:
            # 如果没有token，显示基本的提示
            markdown_lines.append("### 电子表格")
            SheetHandler.add_empty_line(markdown_lines)