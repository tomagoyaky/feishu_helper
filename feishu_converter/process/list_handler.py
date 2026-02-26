"""
列表处理器类
"""
import logging
from typing import Dict, Any, List
from .base_handler import BaseHandler


class ListHandler(BaseHandler):
    """
    处理列表相关的块类型
    """
    
    logger = logging.getLogger(__name__)
    
    @staticmethod
    def process_bullet_list(block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理无序列表块
        
        :param block: 块数据
        :param markdown_lines: Markdown行列表
        """
        elements = block.get('bullet', {}).get('elements', [])
        text_parts = []
        
        for element in elements:
            content = ListHandler.extract_text_with_style(element)
            if content:
                text_parts.append(content)
        
        if text_parts:
            markdown_lines.append(f"- {''.join(text_parts)}")
            BaseHandler.add_empty_line(markdown_lines)
    
    # 类变量，用于跟踪有序列表的序号
    _ordered_list_index = 1
    
    @staticmethod
    def reset_ordered_list_index():
        """
        重置有序列表序号计数器
        """
        ListHandler._ordered_list_index = 1
        print("有序列表序号计数器已重置为 1")
    
    @staticmethod
    def process_ordered_list(block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理有序列表块
        
        :param block: 块数据
        :param markdown_lines: Markdown行列表
        """
        # 记录块数据结构以便调试
        ListHandler.logger.debug(f"有序列表块数据: {block}")
        
        elements = block.get('ordered', {}).get('elements', [])
        text_parts = []
        
        for element in elements:
            content = ListHandler.extract_text_with_style(element)
            if content:
                text_parts.append(content)
        
        # 获取列表项的序号
        ordered_data = block.get('ordered', {})
        
        # 使用飞书返回的序号
        sequence = ordered_data.get('sequence', None)
        if sequence is not None:
            # 尝试将sequence转换为整数
            try:
                index = int(sequence)
                # 更新序号计数器，为下一个列表项做准备
                ListHandler._ordered_list_index = index + 1
            except (ValueError, TypeError):
                # 如果转换失败，使用当前序号
                index = ListHandler._ordered_list_index
                ListHandler._ordered_list_index += 1
        else:
            # 如果没有sequence，使用当前序号
            index = ListHandler._ordered_list_index
            ListHandler._ordered_list_index += 1
        
        ListHandler.logger.debug(f"使用的序号: {index}")
        ListHandler.logger.debug(f"提取的文本部分: {text_parts}")
            
        if text_parts:
            markdown_lines.append(f"{index}. {''.join(text_parts)}")
            BaseHandler.add_empty_line(markdown_lines)
        else:
            # 即使文本为空，也添加一个空行，确保列表项之间的间距
            BaseHandler.add_empty_line(markdown_lines)