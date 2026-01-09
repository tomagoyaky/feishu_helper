"""
飞书文档转换器
主转换器类，协调各个组件完成文档转换任务
"""

import logging
from typing import Dict, Any
from .fetchers.document_fetcher import DocumentFetcher
from .adapters.pdf_adapter import PdfAdapter
from .adapters.markdown_adapter import MarkdownAdapter


class FeishuConverter:
    """
    飞书文档转换器
    协调获取、转换和输出过程
    """
    
    def __init__(self):
        """
        初始化转换器
        """
        self.document_fetcher = DocumentFetcher()
        self.pdf_adapter = PdfAdapter()
        self.markdown_adapter = MarkdownAdapter()
        self.logger = logging.getLogger(__name__)
    
    def convert(self, document_url: str, output_format: str, output_path: str) -> bool:
        """
        执行文档转换
        
        :param document_url: 飞书文档URL
        :param output_format: 输出格式 ('pdf' 或 'markdown')
        :param output_path: 输出路径
        :return: 转换是否成功
        """
        self.logger.info(f"开始转换文档: {document_url} -> {output_path} ({output_format})")
        
        # 获取文档内容
        self.logger.debug(f"开始获取文档信息: {document_url}")
        document_content = self.document_fetcher.fetch_document_content(document_url)
        
        if not document_content:
            self.logger.error("获取文档内容失败")
            return False
        
        # 根据文档信息设置标题
        doc_title = document_content.get('document_info', {}).get('title', 'Unknown')
        self.logger.info(f"文档信息 - 标题: {doc_title}, 版本: {document_content['document_info'].get('revision_id', 'Unknown')}, 文档ID: {document_content['document_info'].get('document_id', 'Unknown')}")
        
        # 根据格式选择适配器
        self.logger.info(f"开始转换为 {output_format} 格式...")
        if output_format.lower() == 'pdf':
            return self.pdf_adapter.convert(document_content, output_path)
        elif output_format.lower() == 'markdown':
            return self.markdown_adapter.convert(document_content, output_path)
        else:
            self.logger.error(f"不支持的输出格式: {output_format}")
            return False
