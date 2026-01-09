"""
文档块基类定义
"""
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from .text_elements import Text
from .bitable import Bitable
from .callout import Callout
from .chat_card import ChatCard
from .diagram import Diagram
from .divider import Divider
from .file_block import File
from .grid import Grid
from .grid_column import GridColumn
from .iframe import Iframe
from .image import Image
from .isv import ISV
from .mindnote import Mindnote
from .sheet import Sheet
from .table import Table
from .table_cell import TableCell
from .view import View
from .quote_container import QuoteContainer
from .task import Task
from .okr import OKR
from .okr import OkrObjective
from .okr import OkrKeyResult
from .okr import OkrProgress
from .aitemplate import AITemplate
from .jira_issue import JiraIssue
from .wiki_catalog import WikiCatalog
from .board import Board
from .agenda import Agenda
from .agenda_item import AgendaItem
from .agenda_item_title import AgendaItemTitle
from .agenda_item_content import AgendaItemContent
from .link_preview import LinkPreview
from .source_synced import SourceSynced
from .reference_synced import ReferenceSynced
from .sub_page_list import SubPageList
from ..enums import BlockType


@dataclass
class Block:
    """
    块的基础元数据结构
    """
    block_id: str  # 块的唯一标识
    block_type: BlockType  # 块的枚举值，表示块的类型
    parent_id: Optional[str] = None  # 块的父块 ID
    children: Optional[List[str]] = None  # 块的子块 ID 列表
    comment_ids: Optional[List[str]] = None  # 文档的评论 ID 列表
    
    # 以下为支持的 Block 类型及其对应的内容实体
    page: Optional[Text] = None  # 页面（根） Block
    text: Optional[Text] = None  # 文本 Block
    heading1: Optional[Text] = None  # 一级标题 Block
    heading2: Optional[Text] = None  # 二级标题 Block
    heading3: Optional[Text] = None  # 三级标题 Block
    heading4: Optional[Text] = None  # 四级标题 Block
    heading5: Optional[Text] = None  # 五级标题 Block
    heading6: Optional[Text] = None  # 六级标题 Block
    heading7: Optional[Text] = None  # 七级标题 Block
    heading8: Optional[Text] = None  # 八级标题 Block
    heading9: Optional[Text] = None  # 九级标题 Block
    bullet: Optional[Text] = None  # 无序列表 Block
    ordered: Optional[Text] = None  # 有序列表 Block
    code: Optional[Text] = None  # 代码块 Block
    quote: Optional[Text] = None  # 引用 Block
    todo: Optional[Text] = None  # 待办事项 Block
    bitable: Optional[Bitable] = None  # 多维表格 Block
    callout: Optional[Callout] = None  # 高亮块 Block
    chat_card: Optional[ChatCard] = None  # 会话卡片 Block
    diagram: Optional[Diagram] = None  # 流程图 & UML 图 Block
    divider: Optional[Divider] = None  # 分割线 Block
    file: Optional[File] = None  # 文件 Block
    grid: Optional[Grid] = None  # 分栏 Block
    grid_column: Optional[GridColumn] = None  # 分栏列 Block
    iframe: Optional[Iframe] = None  # 内嵌 Block
    image: Optional[Image] = None  # 图片 Block
    isv: Optional[ISV] = None  # 开放平台小组件 Block
    mindnote: Optional[Mindnote] = None  # 思维笔记 Block
    sheet: Optional[Sheet] = None  # 电子表格 Block
    table: Optional[Table] = None  # 表格 Block
    table_cell: Optional[TableCell] = None  # 表格单元格 Block
    view: Optional[View] = None  # 视图 Block
    undefined: Optional[Dict[str, Any]] = None  # 未定义 Block
    quote_container: Optional[QuoteContainer] = None  # 引用容器 Block
    task: Optional[Task] = None  # 任务 Block
    okr: Optional[OKR] = None  # OKR Block
    okr_objective: Optional[OkrObjective] = None  # OKR 目标 Block
    okr_key_result: Optional[OkrKeyResult] = None  # OKR 关键结果 Block
    okr_progress: Optional[OkrProgress] = None  # OKR 进展 Block
    ai_template: Optional[AITemplate] = None  # AI 模板 Block
    jira_issue: Optional[JiraIssue] = None  # Jira 问题 Block
    wiki_catalog: Optional[WikiCatalog] = None  # Wiki 子页面列表 Block（旧版）
    board: Optional[Board] = None  # 画板 Block
    agenda: Optional[Agenda] = None  # 议程 Block
    agenda_item: Optional[AgendaItem] = None  # 议程项 Block
    agenda_item_title: Optional[AgendaItemTitle] = None  # 议程项标题 Block
    agenda_item_content: Optional[AgendaItemContent] = None  # 议程项内容 Block
    link_preview: Optional[LinkPreview] = None  # 链接预览 Block
    source_synced: Optional[SourceSynced] = None  # 源同步块
    reference_synced: Optional[ReferenceSynced] = None  # 引用同步块
    sub_page_list: Optional[SubPageList] = None  # Wiki 子页面列表 Block（新版）