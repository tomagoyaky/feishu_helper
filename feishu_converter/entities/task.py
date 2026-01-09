"""
任务块实体定义
"""
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class Task:
    """
    任务块的内容实体
    """
    task_id: str