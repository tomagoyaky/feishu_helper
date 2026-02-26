"""
测试PDF转Markdown功能
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from feishu_converter.tools import convert_pdf_to_markdown

def test_pdf_to_markdown():
    """
    测试PDF转Markdown功能
    """
    print("开始测试PDF转Markdown功能...")
    
    # 检查是否有PDF文件用于测试
    test_pdf_path = "./output/赵朋-工作指南.pdf"
    
    if not os.path.exists(test_pdf_path):
        print(f"测试PDF文件不存在: {test_pdf_path}")
        print("请先运行批量转换生成PDF文件，或提供其他PDF文件路径")
        return
    
    try:
        # 转换PDF为Markdown
        output_path = "./output/赵朋-工作指南_from_pdf.md"
        markdown_content = convert_pdf_to_markdown(test_pdf_path, output_path)
        
        print(f"PDF转Markdown成功！")
        print(f"输出文件: {output_path}")
        print(f"转换内容长度: {len(markdown_content)} 字符")
        
        # 显示前500个字符的内容预览
        print("\n内容预览:")
        print(markdown_content[:500] + "..." if len(markdown_content) > 500 else markdown_content)
        
    except Exception as e:
        print(f"转换失败: {str(e)}")

if __name__ == "__main__":
    test_pdf_to_markdown()
