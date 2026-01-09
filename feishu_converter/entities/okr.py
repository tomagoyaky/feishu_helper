"""
OKR相关块实体定义
"""
from typing import List, Optional
from dataclasses import dataclass
from ..enums import OkrPeriodDisplayStatus, OkrProgressRateMode, OkrProgressStatus, OkrProgressStatusType


@dataclass
class ProgressRate:
    """
    OKR 进展信息块的内容实体
    """
    mode: Optional[OkrProgressRateMode] = None
    current: Optional[float] = None
    percent: Optional[float] = None
    progress_status: Optional[OkrProgressStatus] = None
    status_type: Optional[OkrProgressStatusType] = None
    start: Optional[float] = None
    target: Optional[float] = None


@dataclass
class OKR:
    """
    OKR 块的内容实体
    """
    okr_id: Optional[str] = None
    period_display_status: Optional[OkrPeriodDisplayStatus] = None
    period_name_zh: Optional[str] = None
    period_name_en: Optional[str] = None
    user_id: Optional[str] = None
    visible_setting: Optional[dict] = None  # 包含progress_fill_area_visible, progress_status_visible, score_visible


@dataclass
class OkrObjective:
    """
    OKR 目标块的内容实体
    """
    objective_id: Optional[str] = None
    confidential: Optional[bool] = None
    position: Optional[int] = None
    score: Optional[int] = None
    visible: Optional[bool] = True  # 默认为True
    weight: Optional[float] = None
    progress_rate: Optional[ProgressRate] = None
    content: Optional[dict] = None  # Text object


@dataclass
class OkrKeyResult:
    """
    OKR Key Result（关键结果）块的内容实体
    """
    kr_id: Optional[str] = None
    confidential: Optional[bool] = None
    position: Optional[int] = None
    score: Optional[int] = None
    visible: Optional[bool] = True  # 默认为True
    weight: Optional[float] = None
    progress_rate: Optional[ProgressRate] = None
    content: Optional[dict] = None  # Text object


@dataclass
class OkrProgress:
    """
    OKR 进展块的内容实体，为空结构体
    """
    pass