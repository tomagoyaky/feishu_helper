"""
测试新添加的API功能
"""

import os
import sys
from importlib.util import spec_from_file_location, module_from_spec

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_new_functions():
    """测试新添加的功能是否存在"""
    # 导入我们的本地MCP服务器模块
    server_spec = spec_from_file_location("local_mcp_server", os.path.join(os.path.dirname(__file__), "server.py"))
    local_mcp_server = module_from_spec(server_spec)
    server_spec.loader.exec_module(local_mcp_server)
    
    # 检查新功能是否存在
    new_functions = [
        'create_feishu_block',
        'create_feishu_descendant_block', 
        'update_feishu_block',
        'batch_update_feishu_blocks',
        'delete_feishu_block'
    ]
    
    all_good = True
    for func_name in new_functions:
        if hasattr(local_mcp_server, func_name):
            print(f"✓ {func_name} 函数已定义")
            # 检查函数文档字符串
            func = getattr(local_mcp_server, func_name)
            if func.__doc__:
                print(f"  函数文档: {func.__doc__.split('.')[0]}.")
        else:
            print(f"✗ {func_name} 函数未找到")
            all_good = False
    
    return all_good

def test_existing_functions_still_exist():
    """测试现有功能是否依然存在"""
    server_spec = spec_from_file_location("local_mcp_server", os.path.join(os.path.dirname(__file__), "server.py"))
    local_mcp_server = module_from_spec(server_spec)
    server_spec.loader.exec_module(local_mcp_server)
    
    # 检查现有功能是否还在
    existing_functions = [
        'fetch_feishu_document',
        'create_feishu_document',
        'convert_feishu_link_to_markdown',
        'get_supported_blocks',
        'get_document_info'
    ]
    
    all_good = True
    for func_name in existing_functions:
        if hasattr(local_mcp_server, func_name):
            print(f"✓ {func_name} 函数依然存在")
        else:
            print(f"✗ {func_name} 函数丢失")
            all_good = False
    
    return all_good

def test_api_has_new_methods():
    """测试API模块是否包含新方法"""
    from feishu_converter.api import FeishuDocAPI
    
    expected_methods = [
        'create_block',
        'create_descendant_block',
        'update_block',
        'batch_update_blocks',
        'delete_block'
    ]
    
    all_good = True
    for method_name in expected_methods:
        if hasattr(FeishuDocAPI, method_name):
            print(f"✓ FeishuDocAPI 包含 {method_name} 方法")
            # 检查方法文档
            method = getattr(FeishuDocAPI, method_name)
            if method.__doc__:
                print(f"  方法文档: {method.__doc__.split('.')[0]}.")
        else:
            print(f"✗ FeishuDocAPI 不包含 {method_name} 方法")
            all_good = False
    
    return all_good

if __name__ == "__main__":
    print("开始测试新添加的功能...\n")
    
    # 测试新功能是否存在
    new_func_ok = test_new_functions()
    print()
    
    # 测试现有功能是否依然存在
    existing_func_ok = test_existing_functions_still_exist()
    print()
    
    # 测试API模块是否包含新方法
    api_ok = test_api_has_new_methods()
    print()
    
    if new_func_ok and existing_func_ok and api_ok:
        print("✓ 所有测试通过！新功能已正确添加。")
    else:
        print("✗ 部分测试失败。")