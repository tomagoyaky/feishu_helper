"""
图像处理器类
"""
from typing import Dict, Any, List, Optional
from .base_handler import BaseHandler
from ..utils.image_utils import ImageUtils
from ..api import FeishuDocAPI


class ImageHandler(BaseHandler):
    """
    处理图像相关的块类型
    """
    
    # 类变量，存储输出目录
    output_dir: Optional[str] = None
    output_filename: Optional[str] = None
    
    @classmethod
    def set_output_dir(cls, output_dir: str, output_filename: str = None):
        """
        设置输出目录
        
        :param output_dir: 输出目录路径
        :param output_filename: 输出文件名（不含扩展名）
        """
        cls.output_dir = output_dir
        cls.output_filename = output_filename
    
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
                # 确定图片保存目录
                if ImageHandler.output_dir:
                    import os
                    # 创建图片子目录
                    images_dir = os.path.join(ImageHandler.output_dir, f"{ImageHandler.output_filename}_images")
                    os.makedirs(images_dir, exist_ok=True)
                else:
                    import tempfile
                    images_dir = os.path.join(tempfile.gettempdir(), "feishu_images")
                
                # 初始化图片工具类
                image_utils = ImageUtils(cache_dir=images_dir, access_token=access_token)
                
                # 下载图片
                local_path = image_utils.download_image(token)
                
                if local_path:
                    # 如果设置了输出目录，使用相对路径
                    if ImageHandler.output_dir:
                        import os
                        # 计算相对路径
                        relative_path = os.path.relpath(local_path, ImageHandler.output_dir)
                        markdown_lines.append(f"![{caption}]({relative_path})")
                    else:
                        # 使用绝对路径
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