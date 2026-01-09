"""
图像处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler


class ImageHandler(BaseHandler):
    """
    处理图像相关的块类型
    """
    
    @staticmethod
    def process_image(block: Dict[str, Any], markdown_lines: List[str]):
        """
        处理图片块
        
        :param block: 块数据
        :param markdown_lines: Markdown行列表
        """
        # 飞书API中图片信息可能存储在不同的字段
        image_info = block.get('image', {})
        token = image_info.get('token', '')
        caption = image_info.get('caption', '图片')
        
        # 在Markdown中添加图片占位符
        markdown_lines.append(f"![{caption}](https://internal-api-drive.stream.feishu.cn/space/api/box/stream/download/preview/?file_token={token})")
        ImageHandler.add_empty_line(markdown_lines)