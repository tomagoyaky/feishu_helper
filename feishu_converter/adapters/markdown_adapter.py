"""
Markdown适配器
将飞书文档内容转换为Markdown格式
"""

import logging
from typing import Dict, Any
from ..interfaces import IFormatAdapter
from ..process import (
    TextHandler, TableHandler, HeadingHandler, ListHandler, 
    CodeHandler, QuoteHandler, ImageHandler, DividerHandler,
    ViewHandler, QuoteContainerHandler, TaskHandler, JiraIssueHandler,
    WikiCatalogHandler, BoardHandler, AgendaHandler, AgendaItemHandler,
    LinkPreviewHandler, SubPageListHandler, AitemplateHandler, SheetHandler
)


class MarkdownAdapter(IFormatAdapter):
    """
    Markdown格式适配器
    负责将飞书文档内容转换为Markdown格式
    """
    
    def __init__(self):
        """
        初始化Markdown适配器
        """
        self.logger = logging.getLogger(__name__)
    
    def convert(self, content: Dict[str, Any], output_path: str) -> bool:
        """
        将文档内容转换为Markdown格式
        
        :param content: 飞书文档内容
        :param output_path: 输出路径
        :return: 转换是否成功
        """
        self.logger.info(f"开始将文档内容转换为Markdown: {output_path}")
        
        try:
            # 处理文档内容为Markdown格式
            markdown_content = self._process_blocks(content)
            
            # 写入文件
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            self.logger.info(f"Markdown转换成功: {output_path}")
            return True
        except Exception as e:
            self.logger.error(f"Markdown转换失败: {str(e)}")
            return False
    
    def _process_blocks(self, content: Dict[str, Any]) -> str:
        """
        处理文档块内容为Markdown格式
        
        :param content: 文档内容
        :return: Markdown字符串
        """
        blocks = content.get('items', [])
        markdown_lines = []
        
        # 获取电子表格数据
        spreadsheet_data = content.get('spreadsheet_data', {})
        
        # 构建块索引，便于查找子块
        block_index = {block['block_id']: block for block in blocks}
        
        # 预处理：建立ID到内容的映射（对于表格单元格引用）
        id_to_content = {}
        for block in blocks:
            block_type = block.get('block_type')
            # 为文本块建立ID映射
            if block_type == 2:  # 文本块
                elements = block.get('text', {}).get('elements', [])
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
                    id_to_content[block['block_id']] = full_content
            # 同时处理标题块
            elif block_type in [3, 4, 5, 6, 7, 8, 9, 10, 11]:  # 各级标题
                block_key_map = {
                    3: 'heading1', 4: 'heading2', 5: 'heading3', 6: 'heading4',
                    7: 'heading5', 8: 'heading6', 9: 'heading7', 10: 'heading8', 11: 'heading9'
                }
                block_key = block_key_map.get(block_type)
                if block_key and block_key in block:
                    elements = block[block_key].get('elements', [])
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
                        id_to_content[block['block_id']] = full_content
            # 同时处理引用块
            elif block_type == 15:  # 引用
                elements = block.get('quote', {}).get('elements', [])
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
                    id_to_content[block['block_id']] = full_content
            # 同时处理代码块
            elif block_type == 14:  # 代码块
                elements = block.get('code', {}).get('elements', [])
                text_parts = []
                
                for element in elements:
                    if 'text_run' in element:
                        content_val = element['text_run'].get('content', '')
                        text_parts.append(content_val)
                
                full_content = ''.join(text_parts)
                if full_content:
                    id_to_content[block['block_id']] = full_content
            # 同时处理表格单元格
            elif block_type == 32:  # 表格单元格
                elements = block.get('table_cell', {}).get('elements', [])
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
                    id_to_content[block['block_id']] = full_content
        
        # 遍历所有块，识别表格和独立文本块
        text_blocks = []
        for i, block in enumerate(blocks):
            block_type = block.get('block_type')
            if block_type == 1:  # 页面(Page)
                HeadingHandler.process_page(block, markdown_lines)
            elif block.get('block_type') == 2:  # 文本块
                text_blocks.append((i, block))
            elif 3 <= block_type <= 11:  # 标题块
                level = block_type - 2  # 计算标题级别
                HeadingHandler.process_heading(block, level, markdown_lines)
            elif block_type == 12:  # 无序列表
                ListHandler.process_bullet_list(block, markdown_lines)
            elif block_type == 13:  # 有序列表
                ListHandler.process_ordered_list(block, markdown_lines)
            elif block_type == 14:  # 代码块
                CodeHandler.process_code(block, markdown_lines)
            elif block_type == 15:  # 引用
                QuoteHandler.process_quote(block, markdown_lines)
            elif block_type == 17:  # 待办事项
                TextHandler.process_todo(block, markdown_lines)
            elif block_type == 22:  # 分割线
                DividerHandler.process_divider(markdown_lines)
            elif block_type == 27:  # 图片
                ImageHandler.process_image(block, markdown_lines)
            elif block_type == 19:  # 高亮块
                TextHandler.process_callout(block, markdown_lines)
            elif block_type == 30:  # 电子表格
                # 使用 SheetHandler 处理电子表格
                SheetHandler.process_sheet(block, markdown_lines, spreadsheet_data)
            elif block_type == 31:  # 表格
                # 传递 block_index 和 id_to_content 参数
                TableHandler.process_table(block, markdown_lines, block_index, id_to_content)
            elif block_type == 33:  # 视图
                ViewHandler.process_view(block, markdown_lines)
            elif block_type == 34:  # 引用容器
                QuoteContainerHandler.process_quote_container(block, markdown_lines)
            elif block_type == 35:  # 任务
                TaskHandler.process_task(block, markdown_lines)
            elif block_type == 41:  # Jira问题
                JiraIssueHandler.process_jira_issue(block, markdown_lines)
            elif block_type == 42:  # Wiki目录
                WikiCatalogHandler.process_wiki_catalog(block, markdown_lines)
            elif block_type == 43:  # 画板
                BoardHandler.process_board(block, markdown_lines)
            elif block_type == 44:  # 议程
                AgendaHandler.process_agenda(block, markdown_lines)
            elif block_type == 45:  # 议程项
                AgendaItemHandler.process_agenda_item(block, markdown_lines)
            elif block_type == 48:  # 链接预览
                LinkPreviewHandler.process_link_preview(block, markdown_lines)
            elif block_type == 51:  # 子页面列表
                SubPageListHandler.process_sub_page_list(block, markdown_lines)
            elif block_type == 52:  # AI模板
                AitemplateHandler.process_aitemplate(block, markdown_lines)
            # 其他块类型可根据需要添加处理逻辑
        
        return '\n'.join(markdown_lines)