"""
OKR处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class OKRHandler(BaseHandler):
    """
    处理OKR类型的块
    """
    
    @staticmethod
    def process_okr(okr_block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理OKR块
        
        :param okr_block: OKR块
        :param markdown_lines: Markdown行列表
        """
        # 检查OKR类型
        if 'okr' in okr_block:
            okr_data = okr_block['okr']
            markdown_lines.append("### OKR 目标")
            
            # 处理目标
            if 'objective' in okr_data:
                objective = okr_data['objective']
                if 'content' in objective:
                    markdown_lines.append(f"**目标:** {objective['content']}")
                
                # 处理关键结果
                if 'key_results' in objective:
                    key_results = objective['key_results']
                    if key_results:
                        markdown_lines.append("\n**关键结果:**")
                        for i, kr in enumerate(key_results, 1):
                            if 'content' in kr:
                                markdown_lines.append(f"{i}. {kr['content']}")
        else:
            # 处理其他OKR相关块类型
            markdown_lines.append("<!-- OKR 相关块 -->")
        
        OKRHandler.add_empty_line(markdown_lines)