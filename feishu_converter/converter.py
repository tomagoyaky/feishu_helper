"""
飞书文档转换器
主转换器类，协调各个组件完成文档转换任务
"""

import logging
from typing import Dict, Any
from .fetchers.document_fetcher import DocumentFetcher
from .adapters.pdf_adapter import PdfAdapter
from .adapters.markdown_adapter import MarkdownAdapter
from .api import FeishuDocAPI


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
        self.api = FeishuDocAPI()
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
        
        # 从URL中提取文档ID并检查文档类型
        doc_id = self.document_fetcher.extract_document_id(document_url)
        if not doc_id:
            self.logger.error(f"无法从URL提取文档ID: {document_url}")
            return False
        
        # 检查文档状态和类型
        doc_status = self.api.check_document_status(doc_id)
        if not doc_status["accessible"]:
            error_msg = doc_status.get("error", "文档不可访问")
            self.logger.error(f"文档不可访问: {error_msg}")
            return False
        
        doc_type = doc_status.get("doc_type", "docx")
        self.logger.info(f"文档类型: {doc_type}, 标题: {doc_status.get('title', 'Unknown')}")
        
        # 根据文档类型获取内容
        if doc_type == "sheet":
            # 获取电子表格内容
            document_content = self.document_fetcher.fetch_spreadsheet_content(document_url)
        else:
            # 获取普通文档内容
            document_content = self.document_fetcher.fetch_document_content(document_url)
        
        if not document_content:
            self.logger.error("获取文档内容失败")
            return False
        
        # 根据格式选择适配器
        self.logger.info(f"开始转换为 {output_format} 格式...")
        if output_format.lower() == 'pdf':
            return self.pdf_adapter.convert(document_content, output_path)
        elif output_format.lower() == 'markdown':
            return self.markdown_adapter.convert(document_content, output_path)
        else:
            self.logger.error(f"不支持的输出格式: {output_format}")
            return False
