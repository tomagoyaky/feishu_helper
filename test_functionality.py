"""
测试脚本，验证飞书转换器功能
"""

import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from feishu_converter.converter import FeishuConverter

def test_converter():
    """
    测试转换器功能
    """
    # 从环境变量获取配置
    app_id = os.getenv('FEISHU_APP_ID')
    app_secret = os.getenv('FEISHU_APP_SECRET')
    
    if not app_id or not app_secret:
        print("请设置FEISHU_APP_ID和FEISHU_APP_SECRET环境变量")
        return False
    
    # 创建转换器实例
    converter = FeishuConverter(app_id=app_id, app_secret=app_secret)
    
    # 示例文档链接（请替换为实际存在的文档链接进行测试）
    doc_url = "https://r3c0qt6yjw.feishu.cn/wiki/WIHiwPrOaiXA0Rk3VjCc8m7snoe"  # 请替换为真实文档链接
    
    # 测试PDF转换
    try:
        print("测试PDF转换...")
        pdf_success = converter.convert(doc_url, "pdf", "./workspace/test_output.pdf")
        print(f"PDF转换结果: {'成功' if pdf_success else '失败'}")
    except Exception as e:
        print(f"PDF转换异常: {str(e)}")
    
    # 测试Markdown转换
    try:
        print("测试Markdown转换...")
        md_success = converter.convert(doc_url, "markdown", "./workspace/test_output.md")
        print(f"Markdown转换结果: {'成功' if md_success else '失败'}")
    except Exception as e:
        print(f"Markdown转换异常: {str(e)}")
    
    return True

def test_with_sample_data():
    """
    使用模拟数据测试转换器
    """
    print("使用模拟数据测试转换器...")
    
    # 创建模拟的文档内容数据
    sample_content = {
        "items": [
            {
                "block_id": "mock_page_block",
                "block_type": 1,  # Page block
                "parent_id": "",
                "children": [],
                "page": {
                    "elements": [
                        {
                            "text_run": {
                                "content": "测试文档标题",
                                "text_element_style": {}
                            }
                        }
                    ],
                    "style": {
                        "align": 1
                    }
                }
            },
            {
                "block_id": "mock_text_block",
                "block_type": 2,  # Text block
                "parent_id": "mock_page_block",
                "children": [],
                "text": {
                    "elements": [
                        {
                            "text_run": {
                                "content": "这是测试文档的正文内容。",
                                "text_element_style": {
                                    "bold": True
                                }
                            }
                        }
                    ],
                    "style": {}
                }
            }
        ],
        "total": 2
    }
    
    # 测试PDF适配器
    from feishu_converter.adapters.pdf_adapter import PdfAdapter
    pdf_adapter = PdfAdapter()
    
    try:
        pdf_result = pdf_adapter.convert(sample_content, "./workspace/sample_test.pdf")
        print(f"PDF适配器测试结果: {'成功' if pdf_result else '失败'}")
    except Exception as e:
        print(f"PDF适配器测试异常: {str(e)}")
    
    # 测试Markdown适配器
    from feishu_converter.adapters.markdown_adapter import MarkdownAdapter
    md_adapter = MarkdownAdapter()
    
    try:
        md_result = md_adapter.convert(sample_content, "./workspace/sample_test.md")
        print(f"Markdown适配器测试结果: {'成功' if md_result else '失败'}")
    except Exception as e:
        print(f"Markdown适配器测试异常: {str(e)}")

if __name__ == "__main__":
    print("开始测试飞书转换器功能...")
    
    # 运行模拟数据测试
    test_with_sample_data()
    
    # 如果设置了环境变量，运行完整功能测试
    if os.getenv('FEISHU_APP_ID') and os.getenv('FEISHU_APP_SECRET'):
        test_converter()
    else:
        print("\n警告: 未设置FEISHU_APP_ID和FEISHU_APP_SECRET环境变量，跳过完整功能测试")
        print("请先设置环境变量后再运行完整测试")