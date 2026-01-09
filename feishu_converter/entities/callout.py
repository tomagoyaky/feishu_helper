"""
高亮块实体定义
"""
from typing import List, Optional
from dataclasses import dataclass
from ..enums import CalloutBackgroundColor, CalloutBorderColor, FontColor


@dataclass
class Callout:
    """
    高亮块块的内容实体
    """
    background_color: Optional[CalloutBackgroundColor] = None
    border_color: Optional[CalloutBorderColor] = None
    text_color: Optional[FontColor] = None
    emoji_id: Optional[str] = "gift"  # 默认值为gift