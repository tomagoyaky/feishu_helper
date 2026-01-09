"""
其他类型处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class OtherHandler(BaseHandler):
    """
    处理其他类型的块，目前只处理add_ons对象（新版文档小组件）
    """
    
    @staticmethod
    def process_other(other_block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理新版文档小组件块
        
        :param other_block: 其他类型的块
        :param markdown_lines: Markdown行列表
        """
        block_type = other_block.get('block_type')
        
        # 只处理新版文档小组件（block_type=40）
        if block_type == 40:  # 新版文档小组件
            add_ons_info = other_block.get('add_ons', {})
            token = add_ons_info.get('token')
            
            if token:
                markdown_lines.append(f"<!-- 新版文档小组件，token: {token} -->")
            else:
                markdown_lines.append("<!-- 新版文档小组件，缺少token -->")
        else:
            # 对于其他类型，输出通用信息
            type_names = {
                18: "多维表格",
                23: "文件",
                24: "分栏",
                25: "分栏列",
                26: "内嵌 Block",
                28: "开放平台小组件",
                29: "思维笔记",
                36: "OKR",
                37: "OKR Objective",
                38: "OKR Key Result",
                39: "OKR Progress",
                46: "议程项标题",
                47: "议程项内容",
                49: "源同步块",
                50: "引用同步块",
                999: "未支持块"
            }
            
            type_name = type_names.get(block_type, f"类型 {block_type}")
            markdown_lines.append(f"<!-- {type_name} 块 -->")
        
        OtherHandler.add_empty_line(markdown_lines)