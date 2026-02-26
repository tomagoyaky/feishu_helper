"""
图片处理工具类
提供图片下载、缓存和处理功能
"""

import hashlib
import logging
import os
import tempfile
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import requests
from PIL import Image


class ImageUtils:
    """图片处理工具类"""

    def __init__(self, cache_dir: Optional[str] = None, access_token: Optional[str] = None):
        """
        初始化图片工具类

        :param cache_dir: 图片缓存目录，默认为系统临时目录
        :param access_token: 飞书访问令牌，用于下载受保护的图片
        """
        self.logger = logging.getLogger(__name__)
        self.access_token = access_token

        # 设置缓存目录
        if cache_dir:
            self.cache_dir = Path(cache_dir)
        else:
            self.cache_dir = Path(tempfile.gettempdir()) / "feishu_images"

        # 确保缓存目录存在
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.logger.debug(f"图片缓存目录: {self.cache_dir}")

    def download_image(self, image_token: str, base_url: str = "https://open.feishu.cn/open-apis") -> Optional[str]:
        """
        从飞书下载图片

        :param image_token: 图片token
        :param base_url: API基础URL
        :return: 下载后的本地文件路径，失败返回None
        """
        if not self.access_token:
            self.logger.warning("未提供访问令牌，无法下载图片")
            return None

        # 检查缓存
        cached_path = self._get_cached_path(image_token)
        if cached_path.exists():
            self.logger.debug(f"使用缓存图片: {cached_path}")
            return str(cached_path)

        # 下载图片
        try:
            url = f"{base_url}/drive/v1/medias/{image_token}/download"
            headers = {"Authorization": f"Bearer {self.access_token}"}

            self.logger.debug(f"下载图片: {image_token}")
            response = requests.get(url, headers=headers, stream=True, timeout=30)
            response.raise_for_status()

            # 确定文件扩展名
            content_type = response.headers.get('content-type', '')
            ext = self._get_extension_from_content_type(content_type)

            # 保存图片
            image_path = self.cache_dir / f"{image_token}{ext}"
            with open(image_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            self.logger.info(f"图片下载成功: {image_path}")
            return str(image_path)

        except requests.exceptions.RequestException as e:
            self.logger.error(f"下载图片失败 {image_token}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"处理图片时出错 {image_token}: {e}")
            return None

    def download_image_from_url(self, image_url: str) -> Optional[str]:
        """
        从URL下载图片

        :param image_url: 图片URL
        :return: 下载后的本地文件路径，失败返回None
        """
        # 检查缓存
        url_hash = hashlib.md5(image_url.encode()).hexdigest()
        cached_path = self.cache_dir / f"url_{url_hash}"

        # 尝试找到已缓存的文件（任何扩展名）
        for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
            if (cached_path.with_suffix(ext)).exists():
                return str(cached_path.with_suffix(ext))

        try:
            self.logger.debug(f"从URL下载图片: {image_url}")
            headers = {}
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"

            response = requests.get(image_url, headers=headers, stream=True, timeout=30)
            response.raise_for_status()

            # 确定文件扩展名
            content_type = response.headers.get('content-type', '')
            ext = self._get_extension_from_content_type(content_type)

            # 保存图片
            image_path = cached_path.with_suffix(ext)
            with open(image_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            self.logger.info(f"图片下载成功: {image_path}")
            return str(image_path)

        except Exception as e:
            self.logger.error(f"从URL下载图片失败 {image_url}: {e}")
            return None

    def get_image_info(self, image_path: str) -> dict:
        """
        获取图片信息

        :param image_path: 图片路径
        :return: 图片信息字典
        """
        try:
            with Image.open(image_path) as img:
                return {
                    'width': img.width,
                    'height': img.height,
                    'format': img.format,
                    'mode': img.mode,
                    'size': os.path.getsize(image_path)
                }
        except Exception as e:
            self.logger.error(f"获取图片信息失败 {image_path}: {e}")
            return {}

    def resize_image(self, image_path: str, max_width: int = 800, max_height: int = 600,
                     output_path: Optional[str] = None) -> Optional[str]:
        """
        调整图片大小

        :param image_path: 原图片路径
        :param max_width: 最大宽度
        :param max_height: 最大高度
        :param output_path: 输出路径，默认覆盖原文件
        :return: 调整后的图片路径
        """
        try:
            with Image.open(image_path) as img:
                # 计算新的尺寸
                width, height = img.size
                ratio = min(max_width / width, max_height / height, 1.0)

                if ratio < 1.0:
                    new_width = int(width * ratio)
                    new_height = int(height * ratio)
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                    # 保存
                    save_path = output_path or image_path
                    img.save(save_path, quality=85, optimize=True)
                    return save_path

            return image_path

        except Exception as e:
            self.logger.error(f"调整图片大小失败 {image_path}: {e}")
            return None

    def convert_to_pdf_compatible(self, image_path: str, output_path: Optional[str] = None) -> Optional[str]:
        """
        将图片转换为PDF兼容格式（RGB模式）

        :param image_path: 原图片路径
        :param output_path: 输出路径
        :return: 转换后的图片路径
        """
        try:
            with Image.open(image_path) as img:
                # 转换为RGB模式（PDF需要）
                if img.mode in ('RGBA', 'LA', 'P'):
                    # 创建白色背景
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')

                # 保存为JPEG（PDF兼容）
                save_path = output_path or str(Path(image_path).with_suffix('.jpg'))
                img.save(save_path, 'JPEG', quality=90)
                return save_path

        except Exception as e:
            self.logger.error(f"转换图片格式失败 {image_path}: {e}")
            return None

    def clear_cache(self, max_age_days: int = 7):
        """
        清理过期缓存

        :param max_age_days: 最大缓存天数
        """
        import time

        try:
            current_time = time.time()
            max_age_seconds = max_age_days * 24 * 60 * 60

            for file_path in self.cache_dir.iterdir():
                if file_path.is_file():
                    file_age = current_time - file_path.stat().st_mtime
                    if file_age > max_age_seconds:
                        file_path.unlink()
                        self.logger.debug(f"删除过期缓存: {file_path}")

        except Exception as e:
            self.logger.error(f"清理缓存失败: {e}")

    def _get_cached_path(self, image_token: str) -> Path:
        """获取缓存路径"""
        return self.cache_dir / image_token

    @staticmethod
    def _get_extension_from_content_type(content_type: str) -> str:
        """从Content-Type获取文件扩展名"""
        content_type = content_type.lower()

        if 'png' in content_type:
            return '.png'
        elif 'gif' in content_type:
            return '.gif'
        elif 'bmp' in content_type:
            return '.bmp'
        elif 'webp' in content_type:
            return '.webp'
        elif 'jpeg' in content_type:
            return '.jpg'
        else:
            return '.jpg'  # 默认使用jpg


class ImageCacheManager:
    """图片缓存管理器"""

    def __init__(self, max_cache_size_mb: int = 100):
        """
        初始化缓存管理器

        :param max_cache_size_mb: 最大缓存大小（MB）
        """
        self.logger = logging.getLogger(__name__)
        self.max_cache_size = max_cache_size_mb * 1024 * 1024  # 转换为字节

    def get_cache_size(self, cache_dir: str) -> int:
        """获取缓存目录大小"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(cache_dir):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    total_size += os.path.getsize(fp)
        except Exception as e:
            self.logger.error(f"计算缓存大小失败: {e}")

        return total_size

    def enforce_cache_limit(self, cache_dir: str):
        """强制执行缓存大小限制"""
        try:
            current_size = self.get_cache_size(cache_dir)

            if current_size > self.max_cache_size:
                self.logger.info(f"缓存超出限制，开始清理: {current_size / 1024 / 1024:.2f} MB")

                # 按修改时间排序，删除最旧的文件
                files = []
                for dirpath, dirnames, filenames in os.walk(cache_dir):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        files.append((fp, os.path.getmtime(fp)))

                files.sort(key=lambda x: x[1])  # 按时间排序

                # 删除文件直到低于限制
                for file_path, _ in files:
                    if current_size <= self.max_cache_size:
                        break

                    try:
                        file_size = os.path.getsize(file_path)
                        os.remove(file_path)
                        current_size -= file_size
                        self.logger.debug(f"删除缓存文件: {file_path}")
                    except Exception as e:
                        self.logger.warning(f"删除缓存文件失败 {file_path}: {e}")

        except Exception as e:
            self.logger.error(f"强制执行缓存限制失败: {e}")
