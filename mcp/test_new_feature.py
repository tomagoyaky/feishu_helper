"""
测试新增的从飞书链接转换为Markdown的功能
"""

import os
import sys
from importlib.util import spec_from_file_location, module_from_spec

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_convert_feishu_link_to_markdown_exists():
    """测试新增功能是否存在"""
    # 导入我们的本地MCP服务器模块
    server_spec = spec_from_file_location("local_mcp_server", os.path.join(os.path.dirname(__file__), "server.py"))
    local_mcp_server = module_from_spec(server_spec)
    server_spec.loader.exec_module(local_mcp_server)
    
    # 检查新功能是否存在
    func_name = 'convert_feishu_link_to_markdown'
    if hasattr(local_mcp_server, func_name):
        print(f"✓ {func_name} 函数已定义")
        # 检查函数文档字符串
        func = getattr(local_mcp_server, func_name)
        if func.__doc__:
            print(f"  函数文档: {func.__doc__.split('.')[0]}.")
        else:
            print("  警告: 函数没有文档字符串")
    else:
        print(f"✗ {func_name} 函数未找到")
        return False
    
    return True

def test_other_functions_still_exist():
    """测试原有功能是否依然存在"""
    server_spec = spec_from_file_location("local_mcp_server", os.path.join(os.path.dirname(__file__), "server.py"))
    local_mcp_server = module_from_spec(server_spec)
    server_spec.loader.exec_module(local_mcp_server)
    
    # 检查原有功能是否还在
    functions_to_check = [
        'fetch_feishu_document',
        'convert_feishu_to_markdown',  # 这个函数已经被删除了
        'get_supported_blocks',
        'get_document_info'
    ]
    
    all_good = True
    for func_name in functions_to_check:
        if func_name == 'convert_feishu_to_markdown':
            # 跳过已删除的函数
            continue
        if hasattr(local_mcp_server, func_name):
            print(f"✓ {func_name} 函数依然存在")
        else:
            print(f"✗ {func_name} 函数丢失")
            all_good = False
    
    return all_good

if __name__ == "__main__":
    print("开始测试新增功能...")
    print()
    
    # 测试新增功能
    new_func_ok = test_convert_feishu_link_to_markdown_exists()
    print()
    
    # 测试原有功能
    old_func_ok = test_other_functions_still_exist()
    print()
    
    if new_func_ok and old_func_ok:
        print("✓ 所有测试通过！新增功能和原有功能都正常。")
    else:
        print("✗ 部分测试失败。")