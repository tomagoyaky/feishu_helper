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
        markdown_lines.append("### Jira 问题")
        
        # 处理Jira问题内容
        if 'jira_issue' in block:
            jira_data = block['jira_issue']
            
            # 提取问题信息
            if 'issue_key' in jira_data:
                issue_key = jira_data['issue_key']
                markdown_lines.append(f"**问题ID:** {issue_key}")
            
            # 提取问题标题
            if 'summary' in jira_data:
                summary = jira_data['summary']
                if 'content' in summary:
                    markdown_lines.append(f"**标题:** {summary['content']}")
            
            # 提取问题状态
            if 'status' in jira_data:
                status = jira_data['status']
                markdown_lines.append(f"**状态:** {status}")
            
            # 提取问题链接
            if 'issue_url' in jira_data:
                issue_url = jira_data['issue_url']
                markdown_lines.append(f"**链接:** {issue_url}")
        else:
            markdown_lines.append("<!-- Jira问题块 -->")
        
        JiraIssueHandler.add_empty_line(markdown_lines)