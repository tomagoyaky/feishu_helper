"""
Markdown适配器
将飞书文档内容转换为Markdown格式
"""

import logging
from typing import Dict, Any, List
from ..interfaces import IFormatAdapter
from ..process.base_handler import BaseHandler
from ..process.heading_handler import HeadingHandler
from ..process.list_handler import ListHandler
from ..process.code_handler import CodeHandler
from ..process.quote_handler import QuoteHandler
from ..process.text_handler import TextHandler
from ..process.divider_handler import DividerHandler
from ..process.image_handler import ImageHandler
from ..process.table_handler import TableHandler
from ..process.sheet_handler import SheetHandler
from ..process.view_handler import ViewHandler
from ..process.quote_container_handler import QuoteContainerHandler
from ..process.task_handler import TaskHandler
from ..process.jira_issue_handler import JiraIssueHandler
from ..process.wiki_catalog_handler import WikiCatalogHandler
from ..process.board_handler import BoardHandler
from ..process.agenda_handler import AgendaHandler
from ..process.agenda_item_handler import AgendaItemHandler
from ..process.link_preview_handler import LinkPreviewHandler
from ..process.sub_page_list_handler import SubPageListHandler
from ..process.aitemplate_handler import AitemplateHandler
from ..process.other_handler import OtherHandler
from ..process.bitable_handler import BitableHandler
from ..process.file_handler import FileHandler
from ..process.grid_handler import GridHandler
from ..process.grid_column_handler import GridColumnHandler
from ..process.iframe_handler import IFrameHandler
from ..process.chat_card_handler import ChatCardHandler
from ..process.diagram_handler import DiagramHandler
from ..process.isv_handler import ISVHandler
from ..process.mind_note_handler import MindNoteHandler
from ..process.okr_handler import OKRHandler
from ..process.agenda_item_title_handler import AgendaItemTitleHandler
from ..process.agenda_item_content_handler import AgendaItemContentHandler
from ..process.source_synced_handler import SourceSyncedHandler
from ..process.reference_synced_handler import ReferenceSyncedHandler
from ..process.undefined_handler import UndefinedHandler
from ..process.document_widget_handler import DocumentWidgetHandler


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
        # 重置有序列表序号计数器
        ListHandler.reset_ordered_list_index()
        
        # 重置标题序号计数器
        HeadingHandler.reset_heading_numbers()
        
        blocks = content.get('items', [])
        markdown_lines = []
        
        # 构建块索引（block_id -> block），用于处理嵌套结构
        block_index = {blk['block_id']: blk for blk in blocks if 'block_id' in blk}
        
        # 找出根块（parent_id为空或指向页面块的块）
        page_block_id = None
        for blk in blocks:
            if blk.get('block_type') == 1:  # 页面块
                page_block_id = blk.get('block_id')
                break
        
        # 构建父子关系映射
        parent_children_map = {}
        for blk in blocks:
            parent_id = blk.get('parent_id')
            if parent_id:
                if parent_id not in parent_children_map:
                    parent_children_map[parent_id] = []
                parent_children_map[parent_id].append(blk)
        
        # 获取顶层块（直接作为页面子块的块）
        top_level_blocks = []
        if page_block_id and page_block_id in parent_children_map:
            top_level_blocks = parent_children_map[page_block_id]
        else:
            # 如果没有找到页面块或没有子块，使用所有没有父块或父块是页面块的块
            for blk in blocks:
                parent_id = blk.get('parent_id')
                if not parent_id or parent_id == page_block_id:
                    if blk.get('block_type') != 1:  # 排除页面块本身
                        top_level_blocks.append(blk)
        
        # 如果没有找到顶层块，回退到处理所有块
        if not top_level_blocks:
            top_level_blocks = [blk for blk in blocks if blk.get('block_type') != 1]
        
        # 先处理页面块本身（输出标题）
        if page_block_id and page_block_id in block_index:
            page_block = block_index[page_block_id]
            HeadingHandler.process_page(page_block, markdown_lines)
        
        # 处理顶层块，递归处理子块
        self._process_blocks_recursive(
            top_level_blocks, 
            markdown_lines, 
            block_index, 
            parent_children_map,
            blocks
        )
        
        return '\n'.join(markdown_lines)
    
    def _process_blocks_recursive(
        self, 
        blocks_to_process: List[Dict[str, Any]], 
        markdown_lines: List[str],
        block_index: Dict[str, Any],
        parent_children_map: Dict[str, List],
        all_blocks: List[Dict[str, Any]]
    ):
        """
        递归处理块列表
        
        :param blocks_to_process: 要处理的块列表
        :param markdown_lines: Markdown行列表
        :param block_index: 块索引（block_id -> block）
        :param parent_children_map: 父子关系映射
        :param all_blocks: 所有块的列表
        """
        for i, block in enumerate(blocks_to_process):
            block_type = block.get('block_type')
            block_id = block.get('block_id', '')
            
            # 页面块
            if block_type == 1:  # 页面(Page)
                HeadingHandler.process_page(block, markdown_lines)
            # 文本块
            elif block_type == 2:  # 文本块
                TextHandler.process_text(block, markdown_lines)
            # 标题块
            elif 3 <= block_type <= 11:  # 标题块 (heading1-heading9)
                level = block_type - 2  # 计算标题级别
                # 遇到标题块时重置有序列表序号计数器
                ListHandler.reset_ordered_list_index()
                HeadingHandler.process_heading(block, level, markdown_lines)
            # 列表块
            elif block_type == 12:  # 无序列表
                ListHandler.process_bullet_list(block, markdown_lines)
            elif block_type == 13:  # 有序列表
                ListHandler.process_ordered_list(block, markdown_lines)
            # 代码块
            elif block_type == 14:  # 代码块
                CodeHandler.process_code(block, markdown_lines)
            # 引用块
            elif block_type == 15:  # 引用
                QuoteHandler.process_quote(block, markdown_lines)
            # 待办事项
            elif block_type == 17:  # 待办事项
                TextHandler.process_todo(block, markdown_lines)
            # 多维表格
            elif block_type == 18:  # 多维表格
                BitableHandler.process_bitable(block, markdown_lines)
            # 高亮块
            elif block_type == 19:  # 高亮块
                self._process_callout_with_children(
                    block, markdown_lines, block_index, parent_children_map, all_blocks
                )
            # 会话卡片
            elif block_type == 20:  # 会话卡片
                ChatCardHandler.process_chat_card(block, markdown_lines)
            # 流程图 & UML
            elif block_type == 21:  # 流程图 & UML
                DiagramHandler.process_diagram(block, markdown_lines)
            # 分割线
            elif block_type == 22:  # 分割线
                DividerHandler.process_divider(markdown_lines)
            # 文件
            elif block_type == 23:  # 文件
                FileHandler.process_file(block, markdown_lines)
            # 分栏
            elif block_type == 24:  # 分栏
                GridHandler.process_grid(block, markdown_lines)
            # 分栏列
            elif block_type == 25:  # 分栏列
                GridColumnHandler.process_grid_column(block, markdown_lines)
            # 内嵌 Block
            elif block_type == 26:  # 内嵌 Block
                IFrameHandler.process_iframe(block, markdown_lines)
            # 图片
            elif block_type == 27:  # 图片
                ImageHandler.process_image(block, markdown_lines)
            # 开放平台小组件
            elif block_type == 28:  # 开放平台小组件
                ISVHandler.process_isv(block, markdown_lines)
            # 思维笔记
            elif block_type == 29:  # 思维笔记
                MindNoteHandler.process_mind_note(block, markdown_lines)
            # 电子表格（外部资源，需要权限检查）
            elif block_type == 30:  # 电子表格
                SheetHandler.process_sheet(block, markdown_lines)
            # 表格相关（内部资源，不需要权限检查）
            elif 31 <= block_type <= 32:  # 表格相关 (table, table_cell)
                TableHandler.process_table(block, markdown_lines, all_blocks)
            # 视图块
            elif block_type == 33:  # 视图
                self._process_view_with_children(
                    block, markdown_lines, block_index, parent_children_map, all_blocks
                )
            # 引用容器
            elif block_type == 34:  # 引用容器
                self._process_quote_container_with_children(
                    block, markdown_lines, block_index, parent_children_map, all_blocks
                )
            # 任务
            elif block_type == 35:  # 任务
                TaskHandler.process_task(block, markdown_lines)
            # OKR
            elif 36 <= block_type <= 39:  # OKR 相关块
                OKRHandler.process_okr(block, markdown_lines)
            # 新版文档小组件
            elif block_type == 40:  # 新版文档小组件
                DocumentWidgetHandler.process_document_widget(block, markdown_lines)
            # Jira问题
            elif block_type == 41:  # Jira问题
                JiraIssueHandler.process_jira_issue(block, markdown_lines)
            # Wiki目录
            elif block_type == 42:  # Wiki目录
                WikiCatalogHandler.process_wiki_catalog(block, markdown_lines)
            # 画板
            elif block_type == 43:  # 画板
                BoardHandler.process_board(block, markdown_lines)
            # 议程
            elif block_type == 44:  # 议程
                AgendaHandler.process_agenda(block, markdown_lines)
            # 议程项
            elif block_type == 45:  # 议程项
                AgendaItemHandler.process_agenda_item(block, markdown_lines)
            # 议程项标题
            elif block_type == 46:  # 议程项标题
                AgendaItemTitleHandler.process_agenda_item_title(block, markdown_lines)
            # 议程项内容
            elif block_type == 47:  # 议程项内容
                AgendaItemContentHandler.process_agenda_item_content(block, markdown_lines)
            # 链接预览
            elif block_type == 48:  # 链接预览
                LinkPreviewHandler.process_link_preview(block, markdown_lines)
            # 源同步块
            elif block_type == 49:  # 源同步块
                SourceSyncedHandler.process_source_synced(block, markdown_lines)
            # 引用同步块
            elif block_type == 50:  # 引用同步块
                ReferenceSyncedHandler.process_reference_synced(block, markdown_lines)
            # 子页面列表
            elif block_type == 51:  # 子页面列表
                SubPageListHandler.process_sub_page_list(block, markdown_lines)
            # AI模板
            elif block_type == 52:  # AI模板
                AitemplateHandler.process_aitemplate(block, markdown_lines)
            # 未支持的块类型
            elif block_type == 999:  # 未支持
                UndefinedHandler.process_undefined(block, markdown_lines)
            # 其他块类型可根据需要添加处理逻辑
            else:
                # 对于未知的块类型，使用OtherHandler处理
                OtherHandler.process_other(block, markdown_lines)
            
            # 递归处理子块
            if block_id in parent_children_map:
                child_blocks = parent_children_map[block_id]
                self._process_blocks_recursive(
                    child_blocks, 
                    markdown_lines, 
                    block_index, 
                    parent_children_map,
                    all_blocks
                )
    
    def _process_view_with_children(
        self, 
        block: Dict[str, Any], 
        markdown_lines: List[str],
        block_index: Dict[str, Any],
        parent_children_map: Dict[str, List],
        all_blocks: List[Dict[str, Any]]
    ):
        """
        处理视图块及其子块
        
        :param block: 块数据
        :param markdown_lines: Markdown行列表
        :param block_index: 块索引
        :param parent_children_map: 父子关系映射
        :param all_blocks: 所有块的列表
        """
        block_id = block.get('block_id', '')
        
        # 视图块本身可能没有内容，但需要处理其子块
        # 使用 parent_children_map 获取子块，而不是 block.get('children')
        if block_id in parent_children_map:
            child_blocks = parent_children_map[block_id]
            for child_block in child_blocks:
                self._process_single_block(
                    child_block, 
                    markdown_lines, 
                    block_index, 
                    parent_children_map, 
                    all_blocks
                )
    
    def _process_quote_container_with_children(
        self, 
        block: Dict[str, Any], 
        markdown_lines: List[str],
        block_index: Dict[str, Any],
        parent_children_map: Dict[str, List],
        all_blocks: List[Dict[str, Any]]
    ):
        """
        处理引用容器块及其子块
        
        :param block: 块数据
        :param markdown_lines: Markdown行列表
        :param block_index: 块索引
        :param parent_children_map: 父子关系映射
        :param all_blocks: 所有块的列表
        """
        block_id = block.get('block_id', '')
        
        # 引用容器块需要处理其子块，并用引用格式包裹
        # 使用 parent_children_map 获取子块，而不是 block.get('children')
        if block_id in parent_children_map:
            child_blocks = parent_children_map[block_id]
            child_lines = []
            for child_block in child_blocks:
                self._process_single_block(
                    child_block, 
                    child_lines, 
                    block_index, 
                    parent_children_map, 
                    all_blocks
                )
            
            # 将子块内容用引用格式包裹
            for line in child_lines:
                if line.strip():
                    markdown_lines.append(f"> {line}")
                else:
                    markdown_lines.append(">")
            BaseHandler.add_empty_line(markdown_lines)
    
    def _process_callout_with_children(
        self, 
        block: Dict[str, Any], 
        markdown_lines: List[str],
        block_index: Dict[str, Any],
        parent_children_map: Dict[str, List],
        all_blocks: List[Dict[str, Any]]
    ):
        """
        处理高亮块及其子块
        
        :param block: 块数据
        :param markdown_lines: Markdown行列表
        :param block_index: 块索引
        :param parent_children_map: 父子关系映射
        :param all_blocks: 所有块的列表
        """
        block_id = block.get('block_id', '')
        callout_data = block.get('callout', {})
        emoji_id = callout_data.get('emoji_id', '')
        
        # 获取子块内容
        # 使用 parent_children_map 获取子块，而不是 block.get('children')
        if block_id in parent_children_map:
            child_blocks = parent_children_map[block_id]
            child_lines = []
            for child_block in child_blocks:
                self._process_single_block(
                    child_block, 
                    child_lines, 
                    block_index, 
                    parent_children_map, 
                    all_blocks
                )
            
            # 将子块内容用引用格式包裹
            emoji_str = f"[{emoji_id}] " if emoji_id else ""
            for line in child_lines:
                if line.strip():
                    markdown_lines.append(f"> {emoji_str}{line}")
                    emoji_str = ""  # 只在第一行显示emoji
                else:
                    markdown_lines.append(">")
            BaseHandler.add_empty_line(markdown_lines)
        else:
            # 如果没有子块，尝试从 callout 的 elements 获取内容
            TextHandler.process_callout(block, markdown_lines)
    
    def _process_single_block(
        self, 
        block: Dict[str, Any], 
        markdown_lines: List[str],
        block_index: Dict[str, Any],
        parent_children_map: Dict[str, List],
        all_blocks: List[Dict[str, Any]]
    ):
        """
        处理单个块
        
        :param block: 块数据
        :param markdown_lines: Markdown行列表
        :param block_index: 块索引
        :param parent_children_map: 父子关系映射
        :param all_blocks: 所有块的列表
        """
        block_type = block.get('block_type')
        block_id = block.get('block_id', '')
        
        # 文本块
        if block_type == 2:
            TextHandler.process_text(block, markdown_lines)
        # 标题块
        elif 3 <= block_type <= 11:
            level = block_type - 2
            HeadingHandler.process_heading(block, level, markdown_lines)
        # 列表块
        elif block_type == 12:
            ListHandler.process_bullet_list(block, markdown_lines)
        elif block_type == 13:
            ListHandler.process_ordered_list(block, markdown_lines)
        # 代码块
        elif block_type == 14:
            CodeHandler.process_code(block, markdown_lines)
        # 引用块
        elif block_type == 15:
            QuoteHandler.process_quote(block, markdown_lines)
        # 待办事项
        elif block_type == 17:
            TextHandler.process_todo(block, markdown_lines)
        # 其他块类型
        elif block_type == 22:
            DividerHandler.process_divider(markdown_lines)
        elif block_type == 27:
            ImageHandler.process_image(block, markdown_lines)
        elif 31 <= block_type <= 32:
            TableHandler.process_table(block, markdown_lines, all_blocks)
        else:
            # 对于其他类型，简单记录
            OtherHandler.process_other(block, markdown_lines)
        
        # 递归处理子块
        if block_id in parent_children_map:
            child_blocks = parent_children_map[block_id]
            self._process_blocks_recursive(
                child_blocks, 
                markdown_lines, 
                block_index, 
                parent_children_map,
                all_blocks
            )