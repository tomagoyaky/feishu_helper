from fastmcp import FastMCP
import os
import sys
import re
from typing import Optional

# 添加项目根目录到Python路径，以便导入feishu_converter模块
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from feishu_converter.api import FeishuDocAPI  # 修改：使用正确的API类名
from feishu_converter.converter import FeishuConverter  # 修改：使用正确的类名
from feishu_converter.adapters.markdown_adapter import MarkdownAdapter
from feishu_converter.fetchers.document_fetcher import DocumentFetcher

mcp = FastMCP("飞书助手MCP服务")

@mcp.tool()
def fetch_feishu_document(doc_token: str, app_id: Optional[str] = None, app_secret: Optional[str] = None) -> dict:
    """
    获取飞书文档内容
    :param doc_token: 文档token
    :param app_id: 应用ID，如果不提供则使用环境变量
    :param app_secret: 应用密钥，如果不提供则使用环境变量
    :return: 包含文档内容的字典
    """
    # 使用环境变量或提供的参数
    actual_app_id = app_id or os.getenv("APP_ID")
    actual_app_secret = app_secret or os.getenv("APP_SECRET")
    
    if not actual_app_id or not actual_app_secret:
        raise ValueError("需要提供app_id和app_secret，可通过参数或环境变量设置")
    
    try:
        # 设置环境变量以供API使用
        os.environ["FEISHU_APP_ID"] = actual_app_id
        os.environ["FEISHU_APP_SECRET"] = actual_app_secret
        
        # 初始化API
        api = FeishuDocAPI()  # 修改：使用正确的API类
        # 获取文档信息
        document_info = api.get_document_info(doc_token)
        
        if document_info:
            return {
                "status": "success",
                "doc_token": doc_token,
                "content": str(document_info),
                "title": document_info.get("title", "Unknown"),
                "document_id": document_info.get("document_id", doc_token)
            }
        else:
            return {
                "status": "error",
                "doc_token": doc_token,
                "error": "无法获取文档信息"
            }
    except Exception as e:
        return {
            "status": "error",
            "doc_token": doc_token,
            "error": str(e)
        }


@mcp.tool()
def create_feishu_document(title: str = "未命名文档", folder_token: Optional[str] = None, app_id: Optional[str] = None, app_secret: Optional[str] = None) -> dict:
    """
    创建飞书文档
    :param title: 文档标题
    :param folder_token: 指定文档所在文件夹的Token，不传或传空表示根目录
    :param app_id: 应用ID，如果不提供则使用环境变量
    :param app_secret: 应用密钥，如果不提供则使用环境变量
    :return: 创建的文档信息
    """
    # 使用环境变量或提供的参数
    actual_app_id = app_id or os.getenv("APP_ID")
    actual_app_secret = app_secret or os.getenv("APP_SECRET")
    
    if not actual_app_id or not actual_app_secret:
        raise ValueError("需要提供app_id和app_secret，可通过参数或环境变量设置")
    
    try:
        # 设置环境变量以供API使用
        os.environ["FEISHU_APP_ID"] = actual_app_id
        os.environ["FEISHU_APP_SECRET"] = actual_app_secret
        
        # 初始化API
        api = FeishuDocAPI()
        
        # 创建文档
        document_info = api.create_document(title=title, folder_token=folder_token)
        
        if document_info:
            return {
                "status": "success",
                "title": document_info.get("title", title),
                "document_id": document_info.get("document_id"),
                "revision_id": document_info.get("revision_id"),
                "message": f"文档 '{title}' 创建成功"
            }
        else:
            return {
                "status": "error",
                "error": "创建文档失败"
            }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


@mcp.tool()
def create_feishu_block(document_id: str, block_id: str, block_type: str, content: str = "", index: Optional[int] = -1, app_id: Optional[str] = None, app_secret: Optional[str] = None) -> dict:
    """
    创建飞书文档块
    :param document_id: 文档ID
    :param block_id: 父块ID
    :param block_type: 块类型
    :param content: 块内容
    :param index: 插入位置索引
    :param app_id: 应用ID，如果不提供则使用环境变量
    :param app_secret: 应用密钥，如果不提供则使用环境变量
    :return: 创建的块信息
    """
    # 使用环境变量或提供的参数
    actual_app_id = app_id or os.getenv("APP_ID")
    actual_app_secret = app_secret or os.getenv("APP_SECRET")
    
    if not actual_app_id or not actual_app_secret:
        raise ValueError("需要提供app_id和app_secret，可通过参数或环境变量设置")
    
    try:
        # 设置环境变量以供API使用
        os.environ["FEISHU_APP_ID"] = actual_app_id
        os.environ["FEISHU_APP_SECRET"] = actual_app_secret
        
        # 初始化API
        api = FeishuDocAPI()
        
        # 创建块
        block_info = api.create_block(document_id=document_id, block_id=block_id, block_type=block_type, content=content, index=index)
        
        if block_info:
            return {
                "status": "success",
                "document_id": document_id,
                "block_id": block_id,
                "message": "块创建成功"
            }
        else:
            return {
                "status": "error",
                "error": "创建块失败"
            }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


@mcp.tool()
def create_feishu_descendant_block(document_id: str, block_id: str, descendants: list, app_id: Optional[str] = None, app_secret: Optional[str] = None) -> dict:
    """
    创建飞书嵌套块
    :param document_id: 文档ID
    :param block_id: 父块ID
    :param descendants: 嵌套块列表
    :param app_id: 应用ID，如果不提供则使用环境变量
    :param app_secret: 应用密钥，如果不提供则使用环境变量
    :return: 创建结果
    """
    # 使用环境变量或提供的参数
    actual_app_id = app_id or os.getenv("APP_ID")
    actual_app_secret = app_secret or os.getenv("APP_SECRET")
    
    if not actual_app_id or not actual_app_secret:
        raise ValueError("需要提供app_id和app_secret，可通过参数或环境变量设置")
    
    try:
        # 设置环境变量以供API使用
        os.environ["FEISHU_APP_ID"] = actual_app_id
        os.environ["FEISHU_APP_SECRET"] = actual_app_secret
        
        # 初始化API
        api = FeishuDocAPI()
        
        # 创建嵌套块
        result = api.create_descendant_block(document_id=document_id, block_id=block_id, descendants=descendants)
        
        if result:
            return {
                "status": "success",
                "document_id": document_id,
                "block_id": block_id,
                "message": "嵌套块创建成功"
            }
        else:
            return {
                "status": "error",
                "error": "创建嵌套块失败"
            }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


@mcp.tool()
def update_feishu_block(document_id: str, block_id: str, content: str, revision_id: Optional[int] = -1, app_id: Optional[str] = None, app_secret: Optional[str] = None) -> dict:
    """
    更新飞书块的内容
    :param document_id: 文档ID
    :param block_id: 块ID
    :param content: 更新的内容
    :param revision_id: 文档版本ID，默认-1表示最新版本
    :param app_id: 应用ID，如果不提供则使用环境变量
    :param app_secret: 应用密钥，如果不提供则使用环境变量
    :return: 更新结果
    """
    # 使用环境变量或提供的参数
    actual_app_id = app_id or os.getenv("APP_ID")
    actual_app_secret = app_secret or os.getenv("APP_SECRET")
    
    if not actual_app_id or not actual_app_secret:
        raise ValueError("需要提供app_id和app_secret，可通过参数或环境变量设置")
    
    try:
        # 设置环境变量以供API使用
        os.environ["FEISHU_APP_ID"] = actual_app_id
        os.environ["FEISHU_APP_SECRET"] = actual_app_secret
        
        # 初始化API
        api = FeishuDocAPI()
        
        # 更新块
        result = api.update_block(document_id=document_id, block_id=block_id, content=content, revision_id=revision_id)
        
        if result:
            return {
                "status": "success",
                "document_id": document_id,
                "block_id": block_id,
                "message": "块更新成功"
            }
        else:
            return {
                "status": "error",
                "error": "更新块失败"
            }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


@mcp.tool()
def batch_update_feishu_blocks(document_id: str, updates: list, revision_id: Optional[int] = -1, app_id: Optional[str] = None, app_secret: Optional[str] = None) -> dict:
    """
    批量更新飞书块的内容
    :param document_id: 文档ID
    :param updates: 更新内容列表，每个元素包含block_id和content
    :param revision_id: 文档版本ID，默认-1表示最新版本
    :param app_id: 应用ID，如果不提供则使用环境变量
    :param app_secret: 应用密钥，如果不提供则使用环境变量
    :return: 更新结果
    """
    # 使用环境变量或提供的参数
    actual_app_id = app_id or os.getenv("APP_ID")
    actual_app_secret = app_secret or os.getenv("APP_SECRET")
    
    if not actual_app_id or not actual_app_secret:
        raise ValueError("需要提供app_id和app_secret，可通过参数或环境变量设置")
    
    try:
        # 设置环境变量以供API使用
        os.environ["FEISHU_APP_ID"] = actual_app_id
        os.environ["FEISHU_APP_SECRET"] = actual_app_secret
        
        # 初始化API
        api = FeishuDocAPI()
        
        # 批量更新块
        result = api.batch_update_blocks(document_id=document_id, updates=updates, revision_id=revision_id)
        
        if result:
            return {
                "status": "success",
                "document_id": document_id,
                "message": "批量更新块成功"
            }
        else:
            return {
                "status": "error",
                "error": "批量更新块失败"
            }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


@mcp.tool()
def delete_feishu_block(document_id: str, block_id: str, start_index: int, end_index: int, revision_id: Optional[int] = -1, app_id: Optional[str] = None, app_secret: Optional[str] = None) -> dict:
    """
    删除飞书块
    :param document_id: 文档ID
    :param block_id: 父块ID
    :param start_index: 开始索引
    :param end_index: 结束索引
    :param revision_id: 文档版本ID，默认-1表示最新版本
    :param app_id: 应用ID，如果不提供则使用环境变量
    :param app_secret: 应用密钥，如果不提供则使用环境变量
    :return: 删除结果
    """
    # 使用环境变量或提供的参数
    actual_app_id = app_id or os.getenv("APP_ID")
    actual_app_secret = app_secret or os.getenv("APP_SECRET")
    
    if not actual_app_id or not actual_app_secret:
        raise ValueError("需要提供app_id和app_secret，可通过参数或环境变量设置")
    
    try:
        # 设置环境变量以供API使用
        os.environ["FEISHU_APP_ID"] = actual_app_id
        os.environ["FEISHU_APP_SECRET"] = actual_app_secret
        
        # 初始化API
        api = FeishuDocAPI()
        
        # 删除块
        result = api.delete_block(document_id=document_id, block_id=block_id, start_index=start_index, end_index=end_index, revision_id=revision_id)
        
        if result:
            return {
                "status": "success",
                "document_id": document_id,
                "block_id": block_id,
                "message": "块删除成功"
            }
        else:
            return {
                "status": "error",
                "error": "删除块失败"
            }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


@mcp.tool()
def convert_feishu_link_to_markdown(feishu_url: str, app_id: Optional[str] = None, app_secret: Optional[str] = None) -> dict:
    """
    从飞书链接直接转换为Markdown格式
    :param feishu_url: 飞书文档URL
    :param app_id: 应用ID，如果不提供则使用环境变量
    :param app_secret: 应用密钥，如果不提供则使用环境变量
    :return: 转换结果，包含Markdown内容
    """
    # 使用环境变量或提供的参数
    actual_app_id = app_id or os.getenv("APP_ID")
    actual_app_secret = app_secret or os.getenv("APP_SECRET")
    
    if not actual_app_id or not actual_app_secret:
        raise ValueError("需要提供app_id和app_secret，可通过参数或环境变量设置")
    
    try:
        # 设置环境变量以供API使用
        os.environ["FEISHU_APP_ID"] = actual_app_id
        os.environ["FEISHU_APP_SECRET"] = actual_app_secret
        
        # 从URL中提取文档ID
        fetcher = DocumentFetcher()
        doc_id = fetcher.extract_document_id(feishu_url)
        
        if not doc_id:
            raise Exception("无法从URL中提取文档ID")
        
        # 初始化API
        api = FeishuDocAPI()
        
        # 获取文档信息
        document_info = api.get_document_info(doc_id)
        if not document_info:
            raise Exception("无法获取文档信息")
        
        # 获取文档块
        document_blocks = api.get_all_document_blocks(doc_id)
        if not document_blocks:
            raise Exception("无法获取文档块")
        
        # 获取文档内容
        content = api.get_doc_content(doc_id)
        
        if content:
            return {
                "status": "success",
                "doc_url": feishu_url,
                "doc_token": doc_id,
                "title": document_info.get("title", "Unknown"),
                "markdown_content": content,
                "message": "文档已成功转换为Markdown格式"
            }
        else:
            # 如果直接获取内容失败，尝试使用转换器
            converter = FeishuConverter()
            # 使用内存中的字符串替代文件输出
            document_content = fetcher.fetch_document_content(feishu_url)
            if document_content:
                markdown_adapter = MarkdownAdapter()
                markdown_result = markdown_adapter.convert(document_content, None)  # 不写入文件，只获取内容
                return {
                    "status": "success",
                    "doc_url": feishu_url,
                    "doc_token": doc_id,
                    "title": document_info.get("title", "Unknown"),
                    "markdown_content": markdown_result,
                    "message": "文档已成功转换为Markdown格式"
                }
            else:
                raise Exception("无法获取文档内容")
    except Exception as e:
        return {
            "status": "error",
            "doc_url": feishu_url,
            "error": str(e)
        }


@mcp.tool()
def get_supported_blocks() -> list:
    """
    获取支持的文档块类型
    :return: 支持的块类型列表
    """
    # 从feishu_converter.entities模块获取所有支持的块类型
    supported_blocks = [
        "Agenda", "Board", "Callout", "Diagram", "Divider", "File", "Grid", 
        "Grid Column", "Iframe", "Image", "Jira Issue", "Link Preview", 
        "Mindnote", "OKR", "Quote Container", "Sheet", "Table", "Task", 
        "Text Elements", "View", "Wiki Catalog", "Bitable", "Reference Synced", 
        "Source Synced", "Sub Page List"
    ]
    
    return supported_blocks


@mcp.resource("feishu://document/{doc_token}")
def get_document_info(doc_token: str, app_id: Optional[str] = None, app_secret: Optional[str] = None) -> dict:
    """
    获取飞书文档信息资源
    :param doc_token: 文档token
    :param app_id: 应用ID，如果不提供则使用环境变量
    :param app_secret: 应用密钥，如果不提供则使用环境变量
    :return: 文档信息
    """
    actual_app_id = app_id or os.getenv("APP_ID")
    actual_app_secret = app_secret or os.getenv("APP_SECRET")
    
    if not actual_app_id or not actual_app_secret:
        raise ValueError("需要提供app_id和app_secret，可通过参数或环境变量设置")
    
    try:
        # 设置环境变量以供API使用
        os.environ["FEISHU_APP_ID"] = actual_app_id
        os.environ["FEISHU_APP_SECRET"] = actual_app_secret
        
        api = FeishuDocAPI()  # 修改：使用正确的API类
        document_info = api.get_document_info(doc_token)
        
        if document_info:
            return {
                "doc_token": doc_token,
                "title": document_info.get("title", "Unknown"),
                "document_id": document_info.get("document_id", doc_token),
                "revision_id": document_info.get("revision_id", 0),
                "description": "飞书文档信息"
            }
        else:
            return {
                "doc_token": doc_token,
                "error": "无法获取文档信息"
            }
    except Exception as e:
        return {
            "doc_token": doc_token,
            "error": str(e)
        }


if __name__ == "__main__":
    mcp.run()