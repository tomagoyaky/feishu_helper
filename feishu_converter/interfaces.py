"""
接口定义
定义飞书转换器所需的各种接口
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class IFeishuConverter(ABC):
    """
    飞书转换器接口
    定义转换器的基本操作
    """
    
    @abstractmethod
    def convert(self, doc_url: str, output_format: str, output_path: str) -> bool:
        """
        转换飞书文档到指定格式
        
        :param doc_url: 飞书文档链接
        :param output_format: 输出格式 (pdf, markdown等)
        :param output_path: 输出路径
        :return: 转换是否成功
        """
        pass


class IFormatAdapter(ABC):
    """
    格式适配器接口
    定义将飞书文档内容转换为特定格式的适配器
    """
    
    @abstractmethod
    def convert(self, content: Dict[str, Any], output_path: str) -> bool:
        """
        将文档内容转换为特定格式
        
        :param content: 飞书文档内容
        :param output_path: 输出路径
        :return: 转换是否成功
        """
        pass


class IDocumentFetcher(ABC):
    """
    文档获取器接口
    定义获取飞书文档内容的方法
    """
    
    @abstractmethod
    def fetch_content(self, doc_url: str) -> Dict[str, Any]:
        """
        获取文档内容
        
        :param doc_url: 飞书文档链接
        :return: 文档内容
        """
        pass
    
    @abstractmethod
    def fetch_raw_content(self, doc_url: str) -> str:
        """
        获取文档纯文本内容
        
        :param doc_url: 飞书文档链接
        :return: 文档纯文本内容
        """
        pass
    
    @abstractmethod
    def fetch_document_info(self, doc_url: str) -> Dict[str, Any]:
        """
        获取文档信息
        
        :param doc_url: 飞书文档链接
        :return: 文档信息
        """
        pass