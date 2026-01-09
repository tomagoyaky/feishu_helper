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
    def process_table(block: Dict[str, Any], markdown_lines: List[str], all_blocks: List[Dict[str, Any]] = None):
        """
        处理表格块
        
        :param block: 块数据
        :param markdown_lines: Markdown行列表
        :param all_blocks: 所有块的列表，用于构建索引和ID到内容的映射
        """
        # 普通表格不需要权限检查，只有电子表格需要
        # 电子表格的权限检查已在SheetHandler中处理
        # 这里继续处理普通表格
        
        # 如果提供了所有块的信息，构建索引和映射
        block_index = {}
        id_to_content = {}
        
        if all_blocks:
            # 构建块索引
            block_index = {blk['block_id']: blk for blk in all_blocks}
            
            # 构建ID到内容的映射
            for blk in all_blocks:
                blk_type = blk.get('block_type')
                
                # 为文本块建立ID映射
                if blk_type == 2:  # 文本块
                    elements = blk.get('text', {}).get('elements', [])
                    text_parts = []
                    
                    for element in elements:
                        if 'text_run' in element:
                            content_val = element['text_run'].get('content', '')
                            # 处理文本样式
                            style = element['text_run'].get('text_element_style', {})
                            if style:
                                bold = style.get('bold', False)
                                italic = style.get('italic', False)
                                strikethrough = style.get('strikethrough', False)
                                inline_code = style.get('inline_code', False)
                                
                                if bold:
                                    content_val = f"**{content_val}**"
                                if italic:
                                    content_val = f"*{content_val}*"
                                if strikethrough:
                                    content_val = f"~~{content_val}~~"
                                if inline_code:
                                    content_val = f"`{content_val}`"
                            
                            text_parts.append(content_val)
                    
                    full_content = ''.join(text_parts)
                    if full_content:
                        id_to_content[blk['block_id']] = full_content
                # 处理标题块
                elif blk_type in [3, 4, 5, 6, 7, 8, 9, 10, 11]:  # 各级标题
                    block_key_map = {
                        3: 'heading1', 4: 'heading2', 5: 'heading3', 6: 'heading4',
                        7: 'heading5', 8: 'heading6', 9: 'heading7', 10: 'heading8', 11: 'heading9'
                    }
                    block_key = block_key_map.get(blk_type)
                    if block_key and block_key in blk:
                        elements = blk[block_key].get('elements', [])
                        text_parts = []
                        
                        for element in elements:
                            if 'text_run' in element:
                                content_val = element['text_run'].get('content', '')
                                # 处理文本样式
                                style = element['text_run'].get('text_element_style', {})
                                if style:
                                    bold = style.get('bold', False)
                                    italic = style.get('italic', False)
                                    strikethrough = style.get('strikethrough', False)
                                    inline_code = style.get('inline_code', False)
                                    
                                    if bold:
                                        content_val = f"**{content_val}**"
                                    if italic:
                                        content_val = f"*{content_val}*"
                                    if strikethrough:
                                        content_val = f"~~{content_val}~~"
                                    if inline_code:
                                        content_val = f"`{content_val}`"
                                
                                text_parts.append(content_val)
                        
                        full_content = ''.join(text_parts)
                        if full_content:
                            id_to_content[blk['block_id']] = full_content
                # 处理引用块
                elif blk_type == 15:  # 引用
                    elements = blk.get('quote', {}).get('elements', [])
                    text_parts = []
                    
                    for element in elements:
                        if 'text_run' in element:
                            content_val = element['text_run'].get('content', '')
                            # 处理文本样式
                            style = element['text_run'].get('text_element_style', {})
                            if style:
                                bold = style.get('bold', False)
                                italic = style.get('italic', False)
                                strikethrough = style.get('strikethrough', False)
                                inline_code = style.get('inline_code', False)
                                
                                if bold:
                                    content_val = f"**{content_val}**"
                                if italic:
                                    content_val = f"*{content_val}*"
                                if strikethrough:
                                    content_val = f"~~{content_val}~~"
                                if inline_code:
                                    content_val = f"`{content_val}`"
                            
                            text_parts.append(content_val)
                    
                    full_content = ''.join(text_parts)
                    if full_content:
                        id_to_content[blk['block_id']] = full_content
                # 处理代码块
                elif blk_type == 14:  # 代码块
                    elements = blk.get('code', {}).get('elements', [])
                    text_parts = []
                    
                    for element in elements:
                        if 'text_run' in element:
                            content_val = element['text_run'].get('content', '')
                            text_parts.append(content_val)
                    
                    full_content = ''.join(text_parts)
                    if full_content:
                        id_to_content[blk['block_id']] = full_content
                # 处理表格单元格
                elif blk_type == 32:  # 表格单元格
                    elements = blk.get('table_cell', {}).get('elements', [])
                    text_parts = []
                    
                    for element in elements:
                        if 'text_run' in element:
                            content_val = element['text_run'].get('content', '')
                            # 处理文本样式
                            style = element['text_run'].get('text_element_style', {})
                            if style:
                                bold = style.get('bold', False)
                                italic = style.get('italic', False)
                                strikethrough = style.get('strikethrough', False)
                                inline_code = style.get('inline_code', False)
                                
                                if bold:
                                    content_val = f"**{content_val}**"
                                if italic:
                                    content_val = f"*{content_val}*"
                                if strikethrough:
                                    content_val = f"~~{content_val}~~"
                                if inline_code:
                                    content_val = f"`{content_val}`"
                            
                            text_parts.append(content_val)
                    
                    full_content = ''.join(text_parts)
                    if full_content:
                        id_to_content[blk['block_id']] = full_content
        
        table_data = block.get('table', {})
        cells = table_data.get('cells', [])  # cells 包含单元格块 ID
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
                        # 获取单元格ID
                        cell_id = cells[idx]
                        
                        # 如果提供了ID到内容的映射，优先使用映射
                        if id_to_content and isinstance(cell_id, str) and cell_id in id_to_content:
                            cell_content = id_to_content[cell_id]
                        elif block_index and isinstance(cell_id, str) and cell_id in block_index:
                            # 如果单元格ID指向另一个块，获取该块的内容
                            cell_block = block_index[cell_id]
                            cell_content = TableHandler._extract_content_from_cell_block(cell_block, block_index)
                        else:
                            # 如果单元格内容是简单文本
                            cell_content = str(cell_id) if cell_id else ""
                        
                        row.append(cell_content)
                    else:
                        row.append("")
                table_content.append(row)
            
            # 将表格转换为Markdown格式
            if table_content:
                for i, row in enumerate(table_content):
                    # 将每个单元格内容转义特殊字符（如果需要）
                    formatted_row = [cell.replace('|', '\\|') if cell and cell != " " else ' ' for cell in row]
                    markdown_lines.append("| " + " | ".join(formatted_row) + " |")
                    
                    # 在第一行后添加分隔行
                    if i == 0:
                        markdown_lines.append("| " + " | ".join(['---'] * len(row)) + " |")
                
                TableHandler.add_empty_line(markdown_lines)

    @staticmethod
    def _extract_content_from_cell_block(cell_block: Dict[str, Any], block_index: Dict[str, Any] = None) -> str:
        """
        从单元格块中提取内容
        
        :param cell_block: 单元格块数据
        :param block_index: 块索引，用于查找子块
        :return: 提取的文本内容
        """
        # 根据块类型处理内容
        block_type = cell_block.get('block_type')
        
        if block_type == 32:  # 表格单元格
            # 根据文档，单元格块的内容实体为空结构体，实际内容通过子块填充
            # 获取单元格的子块ID列表
            children = cell_block.get('children', [])
            
            # 如果有子块，处理子块内容
            if children and block_index:
                cell_text_parts = []
                for child_id in children:
                    if child_id in block_index:
                        child_block = block_index[child_id]
                        child_content = TableHandler._extract_content_from_any_block(child_block, block_index)
                        if child_content.strip():  # 只有非空内容才添加
                            cell_text_parts.append(child_content)
                return ' '.join(cell_text_parts) or " "
            else:
                # 如果没有子块，尝试直接从元素获取内容
                cell_data = cell_block.get('table_cell', {})
                elements = cell_data.get('elements', [])
                cell_text_parts = []
                
                for element in elements:
                    content = TableHandler.extract_text_with_style(element)
                    if content:
                        cell_text_parts.append(content)
                
                return ''.join(cell_text_parts) or " "
        else:
            # 对于其他类型的块，使用通用提取方法
            return TableHandler._extract_content_from_any_block(cell_block, block_index)

    @staticmethod
    def _extract_content_from_any_block(block: Dict[str, Any], block_index: Dict[str, Any] = None) -> str:
        """
        从任意类型的块中提取内容
        
        :param block: 块数据
        :param block_index: 块索引，用于查找子块
        :return: 提取的文本内容
        """
        block_type = block.get('block_type')
        
        if block_type == 2:  # 文本块
            elements = block.get('text', {}).get('elements', [])
            cell_text_parts = []
            
            for element in elements:
                content = TableHandler.extract_text_with_style(element)
                if content:
                    cell_text_parts.append(content)
            
            return ''.join(cell_text_parts) or " "
        elif block_type in [3, 4, 5, 6, 7, 8, 9, 10, 11]:  # 标题块
            level = block_type - 2  # 计算标题级别
            elements = block.get(f'heading{level}', {}).get('elements', [])
            cell_text_parts = []
            
            for element in elements:
                content = TableHandler.extract_text_with_style(element)
                if content:
                    cell_text_parts.append(content)
            
            return ''.join(cell_text_parts) or " "
        elif block_type in [12, 13]:  # 有序/无序列表
            elements = block.get('elements', [])
            cell_text_parts = []
            
            for element in elements:
                content = TableHandler.extract_text_with_style(element)
                if content:
                    cell_text_parts.append(content)
            
            return ''.join(cell_text_parts) or " "
        elif block_type == 32:  # 表格单元格，递归处理
            return TableHandler._extract_content_from_cell_block(block, block_index)
        else:
            # 如果块类型未知，尝试从子块获取内容
            children = block.get('children', [])
            if children and block_index:
                cell_text_parts = []
                for child_id in children:
                    if child_id in block_index:
                        child_block = block_index[child_id]
                        child_content = TableHandler._extract_content_from_any_block(child_block, block_index)
                        if child_content.strip():  # 只有非空内容才添加
                            cell_text_parts.append(child_content)
                return ' '.join(cell_text_parts) or " "
            else:
                return " "