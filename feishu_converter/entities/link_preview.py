"""
链接预览块实体定义
"""
from typing import List, Optional
from dataclasses import dataclass
from ..enums import LinkPreviewURLType


@dataclass
class LinkPreview:
    """
    链接预览块的内容实体
    """
    url: str
    url_type: LinkPreviewURLType