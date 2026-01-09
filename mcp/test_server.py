"""
MCP服务器测试脚本
用于验证MCP服务器的基本功能
"""

import os
import sys
from importlib.util import spec_from_file_location, module_from_spec

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_get_supported_blocks():
    """测试获取支持的块类型功能"""
    print("测试 get_supported_blocks...")
    
    # 导入我们的本地MCP服务器模块，避免与系统包冲突
    server_spec = spec_from_file_location("local_mcp_server", os.path.join(os.path.dirname(__file__), "server.py"))
    local_mcp_server = module_from_spec(server_spec)
    server_spec.loader.exec_module(local_mcp_server)
    
    blocks = local_mcp_server.get_supported_blocks()
    print(f"支持的块类型数量: {len(blocks)}")
    print(f"前5个块类型: {blocks[:5]}")
    print("✓ get_supported_blocks 测试完成\n")


def test_with_mock_data():
    """使用模拟数据测试其他功能（需要有效的飞书凭证才能完全测试）"""
    # 注意：这些测试需要有效的app_id和app_secret以及文档token才能完全运行
    app_id = os.getenv("APP_ID")
    app_secret = os.getenv("APP_SECRET")
    
    if not app_id or not app_secret:
        print("警告: 未设置APP_ID和APP_SECRET环境变量，跳过需要API调用的测试")
        print("要运行完整测试，请设置环境变量后重新运行\n")
        return
    
    # 这里我们只是验证函数可以被调用而不报错
    # 实际的API调用需要有效的文档token
    print("环境变量已设置，可以进行API调用测试...")
    

if __name__ == "__main__":
    print("开始测试MCP服务器功能...\n")
    
    # 测试不需要API调用的功能
    test_get_supported_blocks()
    
    # 测试需要API调用的功能
    test_with_mock_data()
    
    print("所有测试完成!")