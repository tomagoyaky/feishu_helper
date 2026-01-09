"""
Jira问题处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class JiraIssueHandler(BaseHandler):
    """
    处理Jira问题类型的块
    """
    
    @staticmethod
    def process_jira_issue(block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理Jira问题块
        
        :param block: 块数据
        :param markdown_lines: Markdown行列表
        """
        markdown_lines.append("<!-- Jira问题块 -->")
        JiraIssueHandler.add_empty_line(markdown_lines)