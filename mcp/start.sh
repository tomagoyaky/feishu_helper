#!/bin/bash

# 飞书助手MCP服务启动脚本

set -e

# 设置脚本所在目录为工作目录
cd "$(dirname "$0")"/..

echo "启动飞书助手MCP服务..."

# 检查是否已安装fastmcp
if ! command -v fastmcp &> /dev/null; then
    echo "未找到fastmcp，尝试安装..."
    pip install fastmcp
fi

# 运行MCP服务器
fastmcp run mcp/server.py

echo "MCP服务已停止"