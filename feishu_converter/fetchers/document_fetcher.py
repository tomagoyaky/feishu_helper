"""
文档获取器
负责获取飞书文档内容
"""

import logging
from typing import Dict, Any, List, Optional
from ..api import FeishuDocAPI


class DocumentFetcher:
    """
    文档获取器
    从飞书开放平台获取文档内容
    """
    
    def __init__(self):
        """
        初始化文档获取器
        """
        self.api = FeishuDocAPI()
        self.logger = logging.getLogger(__name__)
    
    def fetch_document_content(self, document_url: str) -> Optional[Dict[str, Any]]:
        """
        获取文档内容
        
        :param document_url: 文档URL
        :return: 文档内容
        """
        # 从URL中提取文档ID
        document_id = self._extract_document_id(document_url)
        if not document_id:
            self.logger.error(f"无法从URL提取文档ID: {document_url}")
            return None
        
        self.logger.debug(f"开始获取文档内容: {document_url}")
        
        # 获取文档信息
        document_info = self.api.get_document_info(document_id)
        if not document_info:
            self.logger.error(f"获取文档信息失败: {document_id}")
            return None
        
        # 获取所有文档块
        blocks_data = self.api.get_all_document_blocks(document_id)
        if not blocks_data:
            self.logger.error(f"获取文档块失败: {document_id}")
            return None
        
        # 组合文档信息和块数据
        document_content = {
            "document_info": document_info,
            "items": blocks_data["items"]
        }
        
        # 检查是否有电子表格块，如果有，获取电子表格数据
        spreadsheet_data = self._fetch_spreadsheet_data(blocks_data["items"])
        if spreadsheet_data:
            document_content["spreadsheet_data"] = spreadsheet_data
        
        self.logger.info(f"成功获取文档内容: {document_info.get('title', 'Unknown')}")
        
        return document_content
    
    def _extract_document_id(self, document_url: str) -> Optional[str]:
        """
        从文档URL中提取文档ID
        
        :param document_url: 文档URL
        :return: 文档ID
        """
        try:
            # 飞书文档URL格式通常为 https://xxx.feishu.cn/wiki/文档ID 或 https://xxx.feishu.cn/docx/文档ID
            # 例如：https://r3c0qt6yjw.feishu.cn/wiki/WIHiwPrOaiXA0Rk3VjCc8m7snoe
            import re
            # 使用正则表达式匹配文档ID部分
            wiki_pattern = r'/wiki/([a-zA-Z0-9_-]+)'
            docx_pattern = r'/docx/([a-zA-Z0-9_-]+)'
            
            match = re.search(wiki_pattern, document_url) or re.search(docx_pattern, document_url)
            
            if match:
                return match.group(1)
            else:
                self.logger.error(f"无法从URL中提取文档ID: {document_url}")
                return None
        except Exception as e:
            self.logger.error(f"提取文档ID失败: {str(e)}")
            return None
    
    def _fetch_spreadsheet_data(self, blocks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        获取所有电子表格的数据
        
        :param blocks: 文档块列表
        :return: 电子表格数据
        """
        spreadsheet_data = {}
        
        for block in blocks:
            if block.get('block_type') == 30:  # 电子表格块
                sheet_info = block.get('sheet', {})
                token = sheet_info.get('token')
                
                if token:
                    # 电子表格的token格式为 "spreadsheet_token_sheet_id"，需要拆分
                    if '_' in token:
                        parts = token.split('_', 1)
                        spreadsheet_token = parts[0]
                        sheet_id = parts[1]
                    else:
                        # 如果没有下划线，则整个token就是spreadsheet_token
                        spreadsheet_token = token
                        sheet_id = None
                    
                    # 获取电子表格数据
                    data = self.api.get_spreadsheet_data(spreadsheet_token, sheet_id)
                    if data:
                        # 使用原始token作为字典的key，以便在markdown adapter中正确查找
                        spreadsheet_data[token] = data
                        self.logger.info(f"获取电子表格数据成功: {token}")
                    else:
                        self.logger.warning(f"获取电子表格数据失败: {token}")
        
        return spreadsheet_data