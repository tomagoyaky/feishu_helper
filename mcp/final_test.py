"""
最终验证脚本，检查MCP服务器功能
"""

import os
import sys
from importlib.util import spec_from_file_location, module_from_spec

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_functions():
    """测试所有功能是否正常"""
    server_spec = spec_from_file_location("local_mcp_server", os.path.join(os.path.dirname(__file__), "server.py"))
    local_mcp_server = module_from_spec(server_spec)
    server_spec.loader.exec_module(local_mcp_server)
    
    # 检查应该存在的功能
    expected_functions = [
        'fetch_feishu_document',
        'create_feishu_document',          # 新增功能
        'convert_feishu_link_to_markdown', # 新功能
        'get_supported_blocks',
        'get_document_info'
    ]
    
    # 检查不应该存在的功能
    removed_functions = [
        'convert_feishu_to_markdown'  # 已删除的功能
    ]
    
    print("检查存在的功能:")
    all_good = True
    for func_name in expected_functions:
        if hasattr(local_mcp_server, func_name):
            func = getattr(local_mcp_server, func_name)
            print(f"✓ {func_name}: 存在")
            if hasattr(func, '__doc__') and func.__doc__:
                print(f"    描述: {func.__doc__.split('.')[0]}.")
        else:
            print(f"✗ {func_name}: 不存在")
            all_good = False
    
    print("\n检查已删除的功能是否真的被删除:")
    for func_name in removed_functions:
        if hasattr(local_mcp_server, func_name):
            print(f"✗ {func_name}: 仍然存在 (应该已被删除)")
            all_good = False
        else:
            print(f"✓ {func_name}: 已正确删除")
    
    return all_good

if __name__ == "__main__":
    print("运行最终验证...\n")
    
    success = test_functions()
    
    print(f"\n结果: {'所有检查通过!' if success else '某些检查失败!'}")

