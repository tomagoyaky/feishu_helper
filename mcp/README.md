# 飞书助手 MCP 服务

这是一个使用 FastMCP 框架构建的模型上下文协议（MCP）服务器，用于与飞书文档系统交互。该服务允许 AI 模型通过标准化接口访问和处理飞书文档。

## 功能

- 获取飞书文档内容
- 创建飞书文档
- 从飞书链接直接转换为 Markdown 格式
- 获取支持的文档块类型
- 获取飞书文档信息

## 安装依赖

```bash
pip install -r requirements.txt
```

确保你的环境中已安装飞书助手项目所需的所有依赖。

## 配置

在运行服务前，请确保设置了以下环境变量：

```bash
export APP_ID=your_app_id
export APP_SECRET=your_app_secret
```

或者在 `.env` 文件中设置这些变量。

## 运行服务

### 开发模式

```bash
fastmcp dev mcp/server.py
```

### 生产模式

```bash
fastmcp run mcp/server.py
```

### 使用 Python 直接运行

```bash
python mcp/server.py
```

## 工具说明

### 1. fetch_feishu_document

获取指定 token 的飞书文档内容。

参数:
- `doc_token` (str): 文档的 token
- `app_id` (str, optional): 应用 ID，如果不提供则使用环境变量
- `app_secret` (str, optional): 应用密钥，如果不提供则使用环境变量

### 2. create_feishu_document

创建新的飞书文档。

参数:
- `title` (str, optional): 文档标题，默认为"未命名文档"
- `folder_token` (str, optional): 指定文档所在文件夹的Token，不传或传空表示根目录
- `app_id` (str, optional): 应用 ID，如果不提供则使用环境变量
- `app_secret` (str, optional): 应用密钥，如果不提供则使用环境变量

### 3. convert_feishu_link_to_markdown

从飞书链接直接转换为 Markdown 格式。

参数:
- `feishu_url` (str): 飞书文档的完整 URL
- `app_id` (str, optional): 应用 ID，如果不提供则使用环境变量
- `app_secret` (str, optional): 应用密钥，如果不提供则使用环境变量

### 4. get_supported_blocks

获取当前系统支持的文档块类型列表。

### 5. get_document_info (资源)

获取飞书文档的信息资源。

参数:
- `doc_token` (str): 文档的 token
- `app_id` (str, optional): 应用 ID，如果不提供则使用环境变量
- `app_secret` (str, optional): 应用密钥，如果不提供则使用环境变量

## 集成到 Claude Desktop

要将此 MCP 服务器与 Claude Desktop 集成，请运行：

```bash
fastmcp install mcp/server.py --name "飞书助手"
```

然后在 Claude Desktop 的设置中启用该工具。

## 许可证

与主项目相同。