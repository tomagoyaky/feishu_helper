"""
文档组件处理器类
"""
import json

from typing import Dict, Any, List
from .base_handler import BaseHandler


class DocumentWidgetHandler(BaseHandler):
    """
    处理文档组件类型的块
    """
    
    @staticmethod
    def process_document_widget(widget_block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理文档组件块
        
        :param widget_block: 文档组件块
        :param markdown_lines: Markdown行列表
        """
        # 获取add_ons对象
        add_ons_info = widget_block.get('add_ons', {})
        
        # 获取AddOns结构的各个字段
        component_id = add_ons_info.get('component_id', '')
        component_type_id = add_ons_info.get('component_type_id', '')
        record = add_ons_info.get('record', '')
        
        # 输出文档小组件信息
        markdown_lines.append(f"<!-- 文档小组件，类型: {component_type_id} -->")
        
        # 如果有记录数据，可以尝试解析
        if record:
            record_json = json.loads(record)
            markdown_lines.append(f"```json")
            markdown_lines.append(f"{record_json.get('data', '')}")
            markdown_lines.append(f"```")
        
        # 添加空行
        DocumentWidgetHandler.add_empty_line(markdown_lines)