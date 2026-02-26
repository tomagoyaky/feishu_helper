#!/usr/bin/env python3
"""
飞书文档转换器 - 命令行入口

用法:
    python main.py <飞书文档链接> <输出格式> <输出路径>

示例:
    python main.py https://example.feishu.cn/docx/xxx pdf ./output.pdf
    python main.py https://example.feishu.cn/docx/xxx markdown ./output.md
"""

import argparse
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from feishu_converter.converter import FeishuConverter


def setup_logging(verbose: bool = False):
    """设置日志"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def validate_url(url: str) -> bool:
    """验证飞书文档URL"""
    valid_patterns = [
        'feishu.cn/docx/',
        'feishu.cn/wiki/',
        'feishu.cn/docs/',
        'larksuite.com/docx/',
        'larksuite.com/wiki/',
    ]
    return any(pattern in url for pattern in valid_patterns)


def validate_format(format_type: str) -> bool:
    """验证输出格式"""
    valid_formats = ['pdf', 'markdown', 'md']
    return format_type.lower() in valid_formats


def ensure_output_dir(output_path: str) -> bool:
    """确保输出目录存在"""
    try:
        output_dir = os.path.dirname(os.path.abspath(output_path))
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        return True
    except Exception as e:
        print(f"创建输出目录失败: {e}", file=sys.stderr)
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='飞书文档转换器 - 将飞书文档转换为PDF或Markdown格式',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s https://example.feishu.cn/docx/xxx pdf ./output.pdf
  %(prog)s https://example.feishu.cn/wiki/xxx markdown ./output.md
  %(prog)s https://example.feishu.cn/docx/xxx md ./output.md --verbose
        """
    )
    
    parser.add_argument(
        'url',
        help='飞书文档链接 (支持 docx, wiki, docs 格式)'
    )
    
    parser.add_argument(
        'format',
        choices=['pdf', 'markdown', 'md'],
        help='输出格式 (pdf, markdown, md)'
    )
    
    parser.add_argument(
        'output',
        help='输出文件路径'
    )
    
    parser.add_argument(
        '--app-id',
        help='飞书应用ID (默认从环境变量 FEISHU_APP_ID 读取)'
    )
    
    parser.add_argument(
        '--app-secret',
        help='飞书应用密钥 (默认从环境变量 FEISHU_APP_SECRET 读取)'
    )
    
    parser.add_argument(
        '--env-file',
        default='.env',
        help='环境变量文件路径 (默认: .env)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='显示详细日志'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    args = parser.parse_args()
    
    # 设置日志
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    # 加载环境变量
    env_file = args.env_file
    if os.path.exists(env_file):
        load_dotenv(env_file)
        logger.debug(f"已加载环境变量文件: {env_file}")
    else:
        logger.debug(f"环境变量文件不存在: {env_file}")
    
    # 验证URL
    if not validate_url(args.url):
        print(f"错误: 无效的飞书文档链接: {args.url}", file=sys.stderr)
        print("支持的链接格式:", file=sys.stderr)
        print("  - https://xxx.feishu.cn/docx/xxx", file=sys.stderr)
        print("  - https://xxx.feishu.cn/wiki/xxx", file=sys.stderr)
        print("  - https://xxx.feishu.cn/docs/xxx", file=sys.stderr)
        sys.exit(1)
    
    # 获取应用凭证
    app_id = args.app_id or os.getenv('FEISHU_APP_ID')
    app_secret = args.app_secret or os.getenv('FEISHU_APP_SECRET')
    
    if not app_id or not app_secret:
        print("错误: 缺少飞书应用凭证", file=sys.stderr)
        print("请通过以下方式之一提供:", file=sys.stderr)
        print("  1. 命令行参数: --app-id 和 --app-secret", file=sys.stderr)
        print("  2. 环境变量: FEISHU_APP_ID 和 FEISHU_APP_SECRET", file=sys.stderr)
        print("  3. .env 文件", file=sys.stderr)
        sys.exit(1)
    
    # 确保输出目录存在
    if not ensure_output_dir(args.output):
        sys.exit(1)
    
    # 标准化输出格式
    output_format = 'markdown' if args.format in ['markdown', 'md'] else 'pdf'
    
    # 检查输出文件扩展名
    output_path = args.output
    if output_format == 'pdf' and not output_path.endswith('.pdf'):
        output_path += '.pdf'
        logger.debug(f"自动添加扩展名: {output_path}")
    elif output_format == 'markdown' and not output_path.endswith(('.md', '.markdown')):
        output_path += '.md'
        logger.debug(f"自动添加扩展名: {output_path}")
    
    # 执行转换
    logger.info(f"开始转换文档: {args.url}")
    logger.info(f"输出格式: {output_format}")
    logger.info(f"输出路径: {output_path}")
    
    try:
        # 设置环境变量供API使用
        os.environ['FEISHU_APP_ID'] = app_id
        os.environ['FEISHU_APP_SECRET'] = app_secret
        
        # 创建转换器并执行转换
        converter = FeishuConverter()
        success = converter.convert(args.url, output_format, output_path)
        
        if success:
            logger.info(f"转换成功: {output_path}")
            
            # 显示文件信息
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                logger.info(f"文件大小: {file_size / 1024:.2f} KB")
            
            sys.exit(0)
        else:
            logger.error("转换失败")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("用户取消操作")
        sys.exit(130)
    except Exception as e:
        logger.error(f"转换过程中发生错误: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
