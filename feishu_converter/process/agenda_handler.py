"""
议程处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class AgendaHandler(BaseHandler):
    """
    处理议程类型的块
    """
    
    @staticmethod
    def process_agenda(block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理议程块
        
        :param block: 块数据
        :param markdown_lines: Markdown行列表
        """
        markdown_lines.append("### 议程")
        
        # 处理议程内容
        if 'agenda' in block:
            agenda_data = block['agenda']
            
            # 处理议程项目
            if 'items' in agenda_data:
                items = agenda_data['items']
                if items:
                    for i, item in enumerate(items, 1):
                        # 提取议程项目标题
                        if 'title' in item:
                            title = item['title']
                            if 'content' in title:
                                markdown_lines.append(f"{i}. {title['content']}")
                            
                            # 提取议程项目内容
                            if 'content' in item:
                                content = item['content']
                                if 'content' in content:
                                    markdown_lines.append(f"   {content['content']}")
        else:
            markdown_lines.append("<!-- 议程块 -->")
        
        AgendaHandler.add_empty_line(markdown_lines)