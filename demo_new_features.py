#!/usr/bin/env python3
"""
飞书助手新功能演示脚本
演示如何使用新增的API功能
"""

import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from feishu_converter.api import FeishuDocAPI

def demo_new_features():
    """
    演示新功能
    """
    print("="*60)
    print("飞书助手新功能演示")
    print("="*60)
    
    # 初始化API
    api = FeishuDocAPI()
    
    # 演示获取文档所有块的功能
    print("\n1. 获取文档块信息...")
    document_id = "AZlidXYwYoeiD4xL2qGcavmWnAb"
    blocks_data = api.get_all_document_blocks(document_id)
    
    if blocks_data:
        blocks = blocks_data.get("items", [])
        print(f"   找到 {len(blocks)} 个块")
        
        # 显示块信息
        for i, block in enumerate(blocks[:5]):  # 只显示前5个块
            block_type = block.get("block_type", "Unknown")
            block_id = block.get("block_id", "Unknown")
            parent_id = block.get("parent_id", "Unknown")
            print(f"   块 {i+1}: ID={block_id}, 类型={block_type}, 父ID={parent_id}")
    else:
        print("   未能获取文档块信息")
    
    # 演示向文档添加内容
    print("\n2. 尝试向文档添加内容...")
    content_to_add = """# 高通安全启动方案-AI版本

## 概述
高通安全启动（Secure Boot）是确保设备启动过程中执行代码完整性和真实性的关键安全机制。本方案将介绍高通平台安全启动的实现原理、流程以及AI技术在其中的应用。

## 安全启动的重要性
安全启动是防止恶意软件在系统启动过程中运行的第一道防线。它通过验证启动过程中每个阶段的数字签名，确保只有经过认证的代码才能被执行。

## 高通安全启动流程
1. BootROM阶段：固化在芯片中的不可更改代码，提供信任根
2. BootLoader阶段：验证下一阶段代码的签名
3. 操作系统内核阶段：验证内核镜像
4. 应用程序阶段：验证启动的应用程序

## AI在安全启动中的应用
AI技术可以用于：
- 模式识别：检测异常启动行为
- 机器学习：建立正常启动行为模型
- 预测分析：预测潜在安全威胁

## 技术细节
高通安全启动基于硬件安全模块（HSM）和加密验证机制，确保整个启动链的完整性。
"""
    
    # 尝试创建块 - 使用文档ID作为父块ID
    result = api.create_block(
        document_id=document_id,
        block_id=document_id,  # 使用文档ID作为父块ID
        block_type="text",
        content=content_to_add
    )
    
    if result:
        print("   内容添加成功!")
    else:
        print("   内容添加失败")
    
    print("\n演示完成!")


if __name__ == "__main__":
    demo_new_features()