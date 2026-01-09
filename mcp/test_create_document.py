"""
测试新添加的创建文档功能
"""

import os
import sys
from importlib.util import spec_from_file_location, module_from_spec

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_create_document_function_exists():
    """测试新添加的创建文档功能是否存在"""
    # 导入我们的本地MCP服务器模块
    server_spec = spec_from_file_location("local_mcp_server", os.path.join(os.path.dirname(__file__), "server.py"))
    local_mcp_server = module_from_spec(server_spec)
    server_spec.loader.exec_module(local_mcp_server)
    
    # 检查新功能是否存在
    func_name = 'create_feishu_document'
    if hasattr(local_mcp_server, func_name):
        print(f"✓ {func_name} 函数已定义")
        # 检查函数文档字符串
        func = getattr(local_mcp_server, func_name)
        if func.__doc__:
            print(f"  函数文档: {func.__doc__.split('.')[0]}.")
        else:
            print("  警告: 函数没有文档字符串")
        return True
    else:
        print(f"✗ {func_name} 函数未找到")
        return False

def test_all_functions_exist():
    """测试所有功能是否都存在"""
    server_spec = spec_from_file_location("local_mcp_server", os.path.join(os.path.dirname(__file__), "server.py"))
    local_mcp_server = module_from_spec(server_spec)
    server_spec.loader.exec_module(local_mcp_server)
    
    # 检查所有预期的功能是否都在
    expected_functions = [
        'fetch_feishu_document',
        'create_feishu_document',      # 新增功能
        'convert_feishu_link_to_markdown',
        'get_supported_blocks',
        'get_document_info'
    ]
    
    all_good = True
    for func_name in expected_functions:
        if hasattr(local_mcp_server, func_name):
            print(f"✓ {func_name} 函数存在")
        else:
            print(f"✗ {func_name} 函数缺失")
            all_good = False
    
    return all_good

def test_api_has_create_method():
    """测试API模块是否包含创建文档的方法"""
    from feishu_converter.api import FeishuDocAPI
    
    if hasattr(FeishuDocAPI, 'create_document'):
        print("✓ FeishuDocAPI 包含 create_document 方法")
        # 检查方法文档
        method = getattr(FeishuDocAPI, 'create_document')
        if method.__doc__:
            print(f"  方法文档: {method.__doc__.split('.')[0]}.")
        return True
    else:
        print("✗ FeishuDocAPI 不包含 create_document 方法")
        return False

if __name__ == "__main__":
    print("开始测试新添加的创建文档功能...\n")
    
    # 测试新功能是否存在
    new_func_ok = test_create_document_function_exists()
    print()
    
    # 测试所有功能是否都存在
    all_funcs_ok = test_all_functions_exist()
    print()
    
    # 测试API模块是否包含创建方法
    api_ok = test_api_has_create_method()
    print()
    
    if new_func_ok and all_funcs_ok and api_ok:
        print("✓ 所有测试通过！新功能已正确添加。")
    else:
        print("✗ 部分测试失败。")