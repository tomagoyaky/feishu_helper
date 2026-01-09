"""
表格块实体定义
"""
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class TableMergeInfo:
    """
    单元格合并信息
    """
    row_span: Optional[int] = None
    col_span: Optional[int] = None


@dataclass
class Table:
    """
    表格块的内容实体
    """
    cells: Optional[List[str]] = None
    property: Optional[dict] = None  # TableProperty object


@dataclass
class TableProperty:
    """
    表格属性
    """
    row_size: int
    column_size: int
    column_width: Optional[List[int]] = None
    header_row: Optional[bool] = False  # 默认FALSE
    header_column: Optional[bool] = False  # 默认FALSE
    merge_info: Optional[List[TableMergeInfo]] = None