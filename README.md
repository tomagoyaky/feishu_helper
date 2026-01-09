# 飞书助手

一个用于处理飞书文档的工具集，包括文档转换、提取等功能。

## 功能特性

- 飞书文档内容提取
- 文档格式转换（PDF、Markdown等）
- 丰富的文档块类型支持

## MCP 服务

本项目现在包含一个 MCP (Model Context Protocol) 服务，允许 AI 模型通过标准化接口访问和处理飞书文档。

### MCP 服务功能

- 获取飞书文档内容
- 将飞书文档转换为 Markdown 格式
- 获取支持的文档块类型
- 获取飞书文档信息

### 如何使用 MCP 服务

1. 安装依赖：
   ```bash
   pip install fastmcp
   ```

2. 设置环境变量：
   ```bash
   export APP_ID=your_app_id
   export APP_SECRET=your_app_secret
   ```

3. 启动 MCP 服务：
   ```bash
   cd mcp
   python server.py
   ```

或者使用启动脚本：
```bash
./mcp/start.sh
```

有关 MCP 服务的详细信息，请参阅 [mcp/README.md](mcp/README.md)。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置

1. 复制环境变量文件：
   ```bash
   cp .env.example .env
   ```

2. 编辑 [.env](file:///Users/neolix/Documents/vscode/feishu_helper/.env.example) 文件，填入您的飞书应用凭证和工作空间路径：
   ```
   FEISHU_APP_ID=your_app_id
   FEISHU_APP_SECRET=your_app_secret
   WORKSPACE=workspace
   ```

## 使用方法

### 使用脚本运行（推荐）

```bash
# 设置环境
./start.sh setup

# 转换为PDF
./start.sh convert https://example.feishu.cn/docx/xxx pdf output.pdf

# 转换为Markdown
./start.sh convert https://example.feishu.cn/docx/xxx markdown output.md
```

当使用相对路径时，输出文件将保存在WORKSPACE指定的目录中。

### 直接使用Python运行

```python
from feishu_converter.converter import FeishuConverter

# 创建转换器实例
converter = FeishuConverter(app_id='your_app_id', app_secret='your_app_secret')

# 转换为PDF
converter.convert('https://example.feishu.cn/docx/xxx', 'pdf', '/path/to/output.pdf')

# 转换为Markdown
converter.convert('https://example.feishu.cn/docx/xxx', 'markdown', '/path/to/output.md')
```

## API实现

本项目实现了以下飞书官方API：

- `GET /open-apis/docx/v1/documents/:document_id/blocks` - 获取文档块内容
- `GET /open-apis/docx/v1/documents/:document_id` - 获取文档信息
- `POST /open-apis/docx/v1/documents` - 创建文档
- `POST /open-apis/docx/v1/documents/:document_id/blocks/:block_id/children` - 追加块

## 扩展性

本项目设计具有良好的扩展性：

1. 可以通过实现 [IFormatAdapter](file:///Users/neolix/Documents/vscode/feishu_helper/feishu_converter/interfaces.py#L16-L29) 接口添加新的输出格式
2. 可以通过 [FeishuDocAPI](file:///Users/neolix/Documents/vscode/feishu_helper/feishu_converter/api.py#L14-L147) 类扩展更多API功能
3. 可以通过 [IDocumentFetcher](file:///Users/neolix/Documents/vscode/feishu_helper/feishu_converter/interfaces.py#L31-L43) 接口扩展更多文档获取方式