"""
流程图 & UML 处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class DiagramHandler(BaseHandler):
    """
    处理流程图 & UML 类型的块
    """
    
    @staticmethod
    def process_diagram(diagram_block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理流程图 & UML 块
        
        :param diagram_block: 流程图 & UML 块
        :param markdown_lines: Markdown行列表
        """
        markdown_lines.append("### 流程图 & UML")
        
        # 处理流程图内容
        if 'diagram' in diagram_block:
            diagram_data = diagram_block['diagram']
            
            # 提取图表类型
            if 'type' in diagram_data:
                diagram_type = diagram_data['type']
                markdown_lines.append(f"**类型:** {diagram_type}")
            
            # 提取图表标题
            if 'title' in diagram_data:
                title = diagram_data['title']
                if 'content' in title:
                    markdown_lines.append(f"**标题:** {title['content']}")
            
            # 流程图内容通常是复杂的图形结构，这里使用占位符
            markdown_lines.append("[流程图内容] - 包含流程节点、连接线等可视化元素")
        else:
            markdown_lines.append("<!-- 流程图 & UML 块 -->")
        
        DiagramHandler.add_empty_line(markdown_lines)