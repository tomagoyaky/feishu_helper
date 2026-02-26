"""
标题处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class HeadingHandler(BaseHandler):
    """
    处理标题相关的块类型
    """
    # 类变量，用于跟踪标题序号
    # 索引0对应H1, 索引1对应H2, 以此类推
    heading_numbers = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    @staticmethod
    def process_heading(block: Dict[str, Any], level: int, markdown_lines: List[str]):
        """
        处理标题块
        
        :param block: 块数据
        :param level: 标题级别
        :param markdown_lines: Markdown行列表
        """
        import logging
        logger = logging.getLogger(__name__)
        
        # 记录块数据结构以便调试
        logger.debug(f"标题块数据: {block}")
        
        # 确定使用哪个键来获取元素
        block_key_map = {
            3: 'heading1', 4: 'heading2', 5: 'heading3', 6: 'heading4',
            7: 'heading5', 8: 'heading6', 9: 'heading7', 10: 'heading8', 11: 'heading9'
        }
        
        block_key = block_key_map.get(level + 2, f"heading{level-1}")
        logger.debug(f"使用的块键: {block_key}")
        
        if block_key in block:
            elements = block[block_key].get('elements', [])
            text_parts = []
            
            for element in elements:
                content = HeadingHandler.extract_text_with_style(element)
                if content:
                    text_parts.append(content)
            
            # 动态生成标题序号
            sequence = ''
            if text_parts:
                # 计算标题级别索引（H1对应索引0）
                level_index = level - 1
                
                # 更新标题序号
                # 1. 增加当前级别的序号
                HeadingHandler.heading_numbers[level_index] += 1
                # 2. 重置所有子级别的序号
                for i in range(level_index + 1, len(HeadingHandler.heading_numbers)):
                    HeadingHandler.heading_numbers[i] = 0
                
                # 生成序号字符串
                sequence_parts = []
                for i in range(level_index + 1):
                    if HeadingHandler.heading_numbers[i] > 0:
                        sequence_parts.append(str(HeadingHandler.heading_numbers[i]))
                sequence = '.'.join(sequence_parts) + '. '
                
                logger.debug(f"动态生成的序号: {sequence}")
            
            if text_parts:
                # 添加带序号的标题
                markdown_lines.append(f"{'#' * level} {sequence}{' '.join(text_parts)}")
                logger.debug(f"添加带序号的标题: {sequence}{' '.join(text_parts)}")
                BaseHandler.add_empty_line(markdown_lines)
    
    @staticmethod
    def reset_heading_numbers():
        """
        重置标题序号计数器
        """
        HeadingHandler.heading_numbers = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        import logging
        logger = logging.getLogger(__name__)
        logger.debug("标题序号计数器已重置")
    
    @staticmethod
    def process_page(block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理页面块
        
        :param block: 块数据
        :param markdown_lines: Markdown行列表
        """
        import logging
        logger = logging.getLogger(__name__)
        
        elements = block.get('page', {}).get('elements', [])
        for element in elements:
            if 'text_run' in element:
                content = element['text_run']['content']
                
                # 页面标题（总标题）不需要序号
                markdown_lines.append(f"# {content}")
                logger.debug(f"添加页面标题: {content}")
                BaseHandler.add_empty_line(markdown_lines)