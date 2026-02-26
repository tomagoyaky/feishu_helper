#!/usr/bin/env python3
"""
批量转换飞书文档 - 命令行入口

用法:
    python batch_convert.py <json文件> <输出目录> <格式>

示例:
    python batch_convert.py get_info.json ./output markdown
    python batch_convert.py get_info.json ./output pdf --workers 3
    python batch_convert.py get_info.json ./output markdown --doc-type wiki --delay 0.5
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from feishu_converter.tools.batch_converter import main

if __name__ == '__main__':
    main()
