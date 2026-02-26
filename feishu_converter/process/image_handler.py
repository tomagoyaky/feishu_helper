"""
图像处理器类
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler
from ..utils.image_utils import ImageUtils
from ..api import FeishuDocAPI


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
        
        if token:
            # 获取访问令牌
            api = FeishuDocAPI()
            access_token = api.get_access_token()
            
            if access_token:
                # 初始化图片工具类
                image_utils = ImageUtils(access_token=access_token)
                
                # 下载图片
                local_path = image_utils.download_image(token)
                
                if local_path:
                    # 在Markdown中使用本地绝对路径
                    markdown_lines.append(f"![{caption}]({local_path})")
                else:
                    # 如果下载失败，使用在线URL作为备用
                    markdown_lines.append(f"![{caption}](https://internal-api-drive.stream.feishu.cn/space/api/box/stream/download/preview/?file_token={token})")
            else:
                # 如果没有访问令牌，使用在线URL
                markdown_lines.append(f"![{caption}](https://internal-api-drive.stream.feishu.cn/space/api/box/stream/download/preview/?file_token={token})")
        else:
            # 如果没有token，添加占位符
            markdown_lines.append("![图片](图片占位符)")
        
        BaseHandler.add_empty_line(markdown_lines)