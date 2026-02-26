"""
开放平台小组件处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class ISVHandler(BaseHandler):
    """
    处理开放平台小组件类型的块
    """
    
    @staticmethod
    def process_isv(isv_block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理开放平台小组件块
        
        :param isv_block: 开放平台小组件块
        :param markdown_lines: Markdown行列表
        """
        markdown_lines.append("### 开放平台小组件")
        
        # 处理开放平台小组件内容
        if 'isv' in isv_block:
            isv_data = isv_block['isv']
            
            # 提取应用信息
            if 'app_id' in isv_data:
                app_id = isv_data['app_id']
                markdown_lines.append(f"**应用ID:** {app_id}")
            
            # 提取组件信息
            if 'component_id' in isv_data:
                component_id = isv_data['component_id']
                markdown_lines.append(f"**组件ID:** {component_id}")
            
            # 提取组件类型
            if 'component_type' in isv_data:
                component_type = isv_data['component_type']
                markdown_lines.append(f"**组件类型:** {component_type}")
            
            # 小组件内容通常是第三方应用提供的，这里使用占位符
            markdown_lines.append("[开放平台小组件] - 第三方应用组件")
        else:
            markdown_lines.append("<!-- 开放平台小组件块 -->")
        
        ISVHandler.add_empty_line(markdown_lines)