import os
import sys
import argparse
import re
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from feishu_converter.converter import FeishuConverter
from feishu_converter.api import FeishuDocAPI
from feishu_converter.fetchers.document_fetcher import DocumentFetcher

def main():
    """
    主函数，演示如何使用转换器
    """
    parser = argparse.ArgumentParser(description='飞书文档转换器')
    parser.add_argument('--url', required=True, help='飞书文档URL')
    parser.add_argument('--output-format', choices=['pdf', 'markdown'], default='markdown', help='输出格式')

    args = parser.parse_args()

    # 从环境变量获取配置
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    workspace_dir = os.getenv("WORKSPACE", "workspace")

    if not app_id or not app_secret:
        print("错误：请设置环境变量 FEISHU_APP_ID 和 FEISHU_APP_SECRET")
        sys.exit(1)

    # 获取文档ID
    fetcher = DocumentFetcher()
    doc_id = fetcher.extract_document_id(args.url)
    if doc_id is None:
        print("错误：无法从URL提取文档ID")
        sys.exit(1)

    # 尝试获取文档输出文件名
    api = FeishuDocAPI()
    doc_info = api.get_document_info(doc_id)
    if doc_info and 'title' in doc_info:
        title = doc_info['title']
        safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)
        output_filename = f"{safe_title}.{args.output_format}"
    else:
        output_filename = f"output.{args.output_format}"

    # 确保输出目录存在
    os.makedirs(workspace_dir, exist_ok=True)
    output_path = os.path.join(workspace_dir, output_filename)

    # 执行转换
    converter = FeishuConverter()
    success = converter.convert(args.url, args.output_format, output_path)

    if success:
        print(f"转换完成，文件已保存到: {output_path}")
    else:
        print("转换失败")
        sys.exit(1)

if __name__ == "__main__":
    main()