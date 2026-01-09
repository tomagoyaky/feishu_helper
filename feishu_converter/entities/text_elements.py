"""
文本元素实体定义
包含文本相关的所有实体类
"""
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from ..enums import (
    Align, CodeLanguage, TextBackgroundColor, TextIndentationLevel, 
    FontColor, FontBackgroundColor
)


@dataclass
class TextElementStyle:
    """
    文本局部样式内容实体
    """
    bold: Optional[bool] = None
    italic: Optional[bool] = None
    strikethrough: Optional[bool] = None
    underline: Optional[bool] = None
    inline_code: Optional[bool] = None
    text_color: Optional[FontColor] = None
    background_color: Optional[FontBackgroundColor] = None
    link: Optional[Dict[str, str]] = None  # {'url': string}
    comment_ids: Optional[List[str]] = None


@dataclass
class TextRun:
    """
    文字的内容实体
    """
    content: str
    text_element_style: Optional[TextElementStyle] = None


@dataclass
class MentionUser:
    """
    提及用户（@用户）内容实体
    """
    user_id: str
    text_element_style: Optional[TextElementStyle] = None


@dataclass
class MentionDoc:
    """
    提及文档（@文档）块的内容实体
    """
    token: str
    obj_type: Optional[str] = None  # MentionObjType enum
    url: Optional[str] = None
    text_element_style: Optional[TextElementStyle] = None


@dataclass
class Reminder:
    """
    日期提醒内容实体
    """
    create_user_id: str
    is_notify: Optional[bool] = None
    is_whole_day: Optional[bool] = None
    expire_time: Optional[int] = None
    notify_time: Optional[int] = None
    text_element_style: Optional[TextElementStyle] = None


@dataclass
class InlineFile:
    """
    内联文件内容实体
    """
    file_token: Optional[str] = None
    source_block_id: Optional[str] = None
    text_element_style: Optional[TextElementStyle] = None


@dataclass
class InlineBlock:
    """
    内联块的内容实体
    """
    block_id: Optional[str] = None
    text_element_style: Optional[TextElementStyle] = None


@dataclass
class Equation:
    """
    公式内容实体
    """
    content: str
    text_element_style: Optional[TextElementStyle] = None


@dataclass
class UndefinedElement:
    """
    未支持的 TextElementData 内容实体，为空结构体
    """
    pass


@dataclass
class TextElement:
    """
    文本元素内容实体，支持多种类型
    """
    text_run: Optional[TextRun] = None
    mention_user: Optional[MentionUser] = None
    mention_doc: Optional[MentionDoc] = None
    reminder: Optional[Reminder] = None
    file: Optional[InlineFile] = None
    inline_block: Optional[InlineBlock] = None
    equation: Optional[Equation] = None
    undefined_element: Optional[UndefinedElement] = None


@dataclass
class TextStyle:
    """
    文本样式内容实体
    """
    align: Optional[Align] = None
    done: Optional[bool] = None
    folded: Optional[bool] = None
    language: Optional[CodeLanguage] = None
    wrap: Optional[bool] = None
    background_color: Optional[TextBackgroundColor] = None
    indentation_level: Optional[TextIndentationLevel] = None
    sequence: Optional[str] = None


@dataclass
class Text:
    """
    页面、文本、一到九级标题、无序列表、有序列表、代码块、待办事项块的内容实体
    """
    style: Optional[TextStyle] = None
    elements: Optional[List[TextElement]] = None


@dataclass
class AgendaTitleElement:
    """
    议程项标题块的文本元素内容实体
    """
    text_run: Optional[TextRun] = None
    mention_user: Optional[MentionUser] = None
    mention_doc: Optional[MentionDoc] = None
    reminder: Optional[Reminder] = None
    file: Optional[InlineFile] = None
    inline_block: Optional[InlineBlock] = None
    equation: Optional[Equation] = None
    undefined_element: Optional[UndefinedElement] = None