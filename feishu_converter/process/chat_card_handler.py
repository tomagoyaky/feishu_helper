"""
会话卡片处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class ChatCardHandler(BaseHandler):
    """
    处理会话卡片类型的块
    """
    
    @staticmethod
    def process_chat_card(chat_card_block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理会话卡片块
        
        :param chat_card_block: 会话卡片块
        :param markdown_lines: Markdown行列表
        """
        markdown_lines.append("### 会话卡片")
        
        # 处理会话卡片内容
        if 'chat_card' in chat_card_block:
            chat_card_data = chat_card_block['chat_card']
            
            # 提取会话标题
            if 'title' in chat_card_data:
                title = chat_card_data['title']
                if 'content' in title:
                    markdown_lines.append(f"**标题:** {title['content']}")
            
            # 提取会话内容
            if 'content' in chat_card_data:
                content = chat_card_data['content']
                if content:
                    markdown_lines.append("\n**聊天记录:**")
                    markdown_lines.append("```")
                    # 这里简化处理，实际会话内容可能更复杂
                    markdown_lines.append(str(content))
                    markdown_lines.append("```")
        else:
            markdown_lines.append("<!-- 会话卡片块 -->")
        
        ChatCardHandler.add_empty_line(markdown_lines)