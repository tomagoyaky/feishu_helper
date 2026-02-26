"""
链接预览处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class LinkPreviewHandler(BaseHandler):
    """
    处理链接预览类型的块
    """
    
    @staticmethod
    def process_link_preview(block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理链接预览块
        
        :param block: 块数据
        :param markdown_lines: Markdown行列表
        """
        # 从块数据中提取链接预览信息
        link_preview = block.get('link_preview', {})
        
        # 提取链接URL和标题
        url = link_preview.get('url', '')
        title = link_preview.get('title', '')
        description = link_preview.get('description', '')
        
        if url:
            # 构建Markdown链接
            if title:
                markdown_lines.append(f"[{title}]({url})")
            else:
                markdown_lines.append(f"[{url}]({url})")
            
            # 如果有描述，添加描述信息
            if description:
                markdown_lines.append(f"> {description}")
            
            BaseHandler.add_empty_line(markdown_lines)
        else:
            # 如果没有链接信息，添加占位符
            markdown_lines.append("<!-- 链接预览块：无链接信息 -->")
            BaseHandler.add_empty_line(markdown_lines)