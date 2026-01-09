# 飞书助手 MCP 服务

这是一个使用 FastMCP 框架构建的模型上下文协议（MCP）服务器，用于与飞书文档系统交互。该服务允许 AI 模型通过标准化接口访问和处理飞书文档。

## 功能

- 获取飞书文档内容
- 创建飞书文档
- 创建飞书文档块
- 创建飞书嵌套块
- 更新飞书块内容
- 批量更新飞书块内容
- 删除飞书块
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

### 3. create_feishu_block

创建飞书文档块。

参数:
- `document_id` (str): 文档ID
- `block_id` (str): 父块ID
- `block_type` (str): 块类型
- `content` (str, optional): 块内容，默认为空
- `index` (int, optional): 插入位置索引，默认为-1（最后）
- `app_id` (str, optional): 应用 ID，如果不提供则使用环境变量
- `app_secret` (str, optional): 应用密钥，如果不提供则使用环境变量

### 4. create_feishu_descendant_block

创建飞书嵌套块。

参数:
- `document_id` (str): 文档ID
- `block_id` (str): 父块ID
- `descendants` (list): 嵌套块列表
- `app_id` (str, optional): 应用 ID，如果不提供则使用环境变量
- `app_secret` (str, optional): 应用密钥，如果不提供则使用环境变量

### 5. update_feishu_block

更新飞书块的内容。

参数:
- `document_id` (str): 文档ID
- `block_id` (str): 块ID
- `content` (str): 更新的内容
- `revision_id` (int, optional): 文档版本ID，默认-1表示最新版本
- `app_id` (str, optional): 应用 ID，如果不提供则使用环境变量
- `app_secret` (str, optional): 应用密钥，如果不提供则使用环境变量

### 6. batch_update_feishu_blocks

批量更新飞书块的内容。

参数:
- `document_id` (str): 文档ID
- `updates` (list): 更新内容列表，每个元素包含block_id和content
- `revision_id` (int, optional): 文档版本ID，默认-1表示最新版本
- `app_id` (str, optional): 应用 ID，如果不提供则使用环境变量
- `app_secret` (str, optional): 应用密钥，如果不提供则使用环境变量

### 7. delete_feishu_block

删除飞书块。

参数:
- `document_id` (str): 文档ID
- `block_id` (str): 父块ID
- `start_index` (int): 开始索引
- `end_index` (int): 结束索引
- `revision_id` (int, optional): 文档版本ID，默认-1表示最新版本
- `app_id` (str, optional): 应用 ID，如果不提供则使用环境变量
- `app_secret` (str, optional): 应用密钥，如果不提供则使用环境变量

### 8. convert_feishu_link_to_markdown

从飞书链接直接转换为 Markdown 格式。

参数:
- `feishu_url` (str): 飞书文档的完整 URL
- `app_id` (str, optional): 应用 ID，如果不提供则使用环境变量
- `app_secret` (str, optional): 应用密钥，如果不提供则使用环境变量

### 9. get_supported_blocks

获取当前系统支持的文档块类型列表。

### 10. get_document_info (资源)

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