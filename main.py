import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from feishu_converter.converter import FeishuConverter

def main():
    """
    主函数，演示如何使用转换器
    """
    # 从环境变量获取配置
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    
    if not app_id or not app_secret:
        print("错误：请设置环境变量 FEISHU_APP_ID 和 FEISHU_APP_SECRET")
        sys.exit(1)
    
    # 创建转换器实例
    converter = FeishuConverter()
    
    # 从命令行参数获取文档链接、输出格式和输出路径
    if len(sys.argv) < 3:
        print("用法: python main.py <文档链接> <输出格式> [输出路径]")
        print("输出格式: pdf, markdown")
        sys.exit(1)
    
    document_url = sys.argv[1]
    output_format = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else f"workspace/output.{output_format}"
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # 执行转换
    success = converter.convert(document_url, output_format, output_path)
    
    if success:
        print(f"转换完成，文件已保存到: {output_path}")
    else:
        print("转换失败")
        sys.exit(1)

if __name__ == "__main__":
    main()