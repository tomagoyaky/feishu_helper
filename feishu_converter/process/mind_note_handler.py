"""
思维笔记处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class MindNoteHandler(BaseHandler):
    """
    处理思维笔记类型的块
    """
    
    @staticmethod
    def process_mind_note(mind_note_block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理思维笔记块
        
        :param mind_note_block: 思维笔记块
        :param markdown_lines: Markdown行列表
        """
        markdown_lines.append("### 思维笔记")
        
        # 处理思维笔记内容
        if 'mindnote' in mind_note_block:
            mindnote_data = mind_note_block['mindnote']
            
            # 提取思维笔记标题
            if 'title' in mindnote_data:
                title = mindnote_data['title']
                if 'content' in title:
                    markdown_lines.append(f"**标题:** {title['content']}")
            
            # 思维笔记通常包含层次化的节点结构，这里使用列表模拟
            markdown_lines.append("\n**思维导图结构:**")
            markdown_lines.append("- 中心主题")
            markdown_lines.append("  - 分支主题 1")
            markdown_lines.append("    - 子主题 1.1")
            markdown_lines.append("    - 子主题 1.2")
            markdown_lines.append("  - 分支主题 2")
            markdown_lines.append("    - 子主题 2.1")
            markdown_lines.append("    - 子主题 2.2")
        else:
            markdown_lines.append("<!-- 思维笔记块 -->")
        
        MindNoteHandler.add_empty_line(markdown_lines)