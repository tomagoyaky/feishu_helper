"""
Jira问题块实体定义
"""
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class JiraIssue:
    """
    Jira 问题块的内容实体
    """
    id: Optional[str] = None
    key: Optional[str] = None