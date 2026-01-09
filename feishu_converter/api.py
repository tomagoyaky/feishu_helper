"""
飞书开放平台API客户端
提供与飞书开放平台交互的各种API接口
"""

import json
import logging
import os
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()


class FeishuDocAPI:
    """
    飞书文档API客户端
    负责与飞书开放平台进行交互
    """
    
    BASE_URL = "https://open.feishu.cn/open-apis"
    
    def __init__(self):
        """
        初始化API客户端
        """
        self.app_id = os.getenv("FEISHU_APP_ID")
        self.app_secret = os.getenv("FEISHU_APP_SECRET")
        self.access_token = None
        self.logger = logging.getLogger(__name__)
    
    def get_access_token(self) -> Optional[str]:
        """
        获取访问令牌
        
        :return: 访问令牌
        """
        if self.access_token:
            return self.access_token
        
        url = f"{self.BASE_URL}/auth/v3/tenant_access_token/internal"
        headers = {
            "Content-Type": "application/json; charset=utf-8"
        }
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            if result.get("code") == 0:
                self.access_token = result["tenant_access_token"]
                return self.access_token
            else:
                self.logger.error(f"获取访问令牌失败: {result}")
                return None
        except Exception as e:
            self.logger.error(f"请求访问令牌异常: {str(e)}")
            return None
    
    def get_document_info(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        获取文档信息
        
        :param document_id: 文档ID
        :return: 文档信息
        """
        access_token = self.get_access_token()
        if not access_token:
            return None
        
        url = f"{self.BASE_URL}/docx/v1/documents/{document_id}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            if result.get("code") == 0:
                return result["data"]["document"]
            else:
                self.logger.error(f"获取文档信息失败: {result}")
                return None
        except Exception as e:
            self.logger.error(f"请求文档信息异常: {str(e)}")
            return None
    
    def get_document_blocks(self, document_id: str, page_token: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        获取文档块信息
        
        :param document_id: 文档ID
        :param page_token: 分页令牌
        :return: 文档块信息
        """
        access_token = self.get_access_token()
        if not access_token:
            return None
        
        url = f"{self.BASE_URL}/docx/v1/documents/{document_id}/blocks"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        
        params = {"page_size": 100}
        if page_token:
            params["page_token"] = page_token
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            result = response.json()
            if result.get("code") == 0:
                return result["data"]
            else:
                self.logger.error(f"获取文档块失败: {result}")
                return None
        except Exception as e:
            self.logger.error(f"请求文档块异常: {str(e)}")
            return None
    
    def get_all_document_blocks(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        获取文档的所有块（自动处理分页）
        
        :param document_id: 文档ID
        :return: 所有文档块
        """
        all_items = []
        page_token = None
        
        while True:
            data = self.get_document_blocks(document_id, page_token)
            if not data:
                break
            
            items = data.get("items", [])
            all_items.extend(items)
            
            if not data.get("has_more"):
                break
            
            page_token = data.get("page_token")
        
        return {"items": all_items}
    
    def get_spreadsheet_data(self, spreadsheet_token: str, sheet_id: str = None) -> Optional[Dict[str, Any]]:
        """
        获取电子表格数据
        
        :param spreadsheet_token: 电子表格token
        :param sheet_id: 工作表ID
        :return: 电子表格数据
        """
        access_token = self.get_access_token()
        if not access_token:
            return None

        # 从完整的token中提取spreadsheet_token和sheet_id
        # 完整token格式为: spreadsheet_token_sheet_id
        actual_spreadsheet_token = None
        actual_sheet_id = None
    
        # 尝试从传入的spreadsheet_token中解析
        if sheet_id is None and '_' in spreadsheet_token:
            # 如果没有单独提供sheet_id，且传入的token包含下划线，则尝试解析
            parts = spreadsheet_token.split('_', 1)
            if len(parts) == 2:
                actual_spreadsheet_token = parts[0]
                actual_sheet_id = parts[1]
            else:
                actual_spreadsheet_token = spreadsheet_token
        else:
            # 使用参数传递的值
            actual_spreadsheet_token = spreadsheet_token
            actual_sheet_id = sheet_id

        # 构造范围参数
        if actual_sheet_id:
            range_param = f"{actual_sheet_id}"
        else:
            # 如果没有提供sheet_id，则获取表格信息而不是数据
            try:
                basic_info_url = f"{self.BASE_URL}/sheets/v3/spreadsheets/{actual_spreadsheet_token}"
                headers = {
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json; charset=utf-8"
                }
                
                basic_response = requests.get(basic_info_url, headers=headers)
                basic_response.raise_for_status()
                
                basic_result = basic_response.json()
                if basic_result.get("code") == 0:
                    return basic_result["data"]
                else:
                    self.logger.error(f"获取电子表格基本信息失败: {basic_result}")
                    return None
            except Exception as e:
                self.logger.error(f"请求电子表格基本信息异常: {str(e)}")
                return None

        # 使用v2版本API获取电子表格数据
        url = f"{self.BASE_URL}/sheets/v2/spreadsheets/{actual_spreadsheet_token}/values/{range_param}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            result = response.json()
            if result.get("code") == 0:
                return result["data"]
            else:
                self.logger.error(f"获取电子表格数据失败: {result}")
                # 尝试获取电子表格基本信息
                basic_info_url = f"{self.BASE_URL}/sheets/v3/spreadsheets/{actual_spreadsheet_token}"
                basic_response = requests.get(basic_info_url, headers=headers)
                basic_response.raise_for_status()

                basic_result = basic_response.json()
                if basic_result.get("code") == 0:
                    return basic_result["data"]
                else:
                    self.logger.error(f"获取电子表格基本信息也失败: {basic_result}")
                    return None
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"请求电子表格数据HTTP错误: {str(e)}")
            if response is not None:
                self.logger.error(f"响应状态码: {response.status_code}")
                self.logger.error(f"响应内容: {response.text}")
        # 如果获取详细数据失败，尝试获取基本信息
        try:
            basic_info_url = f"{self.BASE_URL}/sheets/v3/spreadsheets/{actual_spreadsheet_token}"
            basic_response = requests.get(basic_info_url, headers=headers)
            basic_response.raise_for_status()

            basic_result = basic_response.json()
            if basic_result.get("code") == 0:
                return basic_result["data"]
            else:
                self.logger.error(f"获取电子表格基本信息也失败: {basic_result}")
                return None
        except Exception as basic_error:
            self.logger.error(f"请求电子表格基本信息也异常: {str(basic_error)}")
