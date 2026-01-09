# 飞书助手

这是一个飞书文档转换项目，可以将飞书文档转换为多种格式，包括Markdown。该项目还提供了一个MCP（Model Context Protocol）服务，便于AI模型与飞书文档进行交互。

## 功能

- 将飞书文档转换为Markdown格式
- 从飞书链接直接转换为Markdown格式
- 获取飞书文档内容
- 创建飞书文档
- 创建、更新、删除飞书文档块
- 批量更新飞书文档块
- 通过MCP协议与飞书文档交互

## 安装

```bash
pip install -r requirements.txt
```

## 配置

在使用前，请确保设置了以下环境变量：

```bash
export APP_ID=your_app_id
export APP_SECRET=your_app_secret
```

或者在 `.env` 文件中设置这些变量。

## MCP 服务

本项目包含一个MCP（Model Context Protocol）服务，允许AI模型通过标准化接口与飞书文档进行交互。

### 启动 MCP 服务

```bash
# 使用启动脚本
./mcp/start.sh

# 或者直接运行Python文件
python mcp/server.py
```

### MCP 服务功能

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

## 使用

### 转换飞书文档

```python
from feishu_converter.api import FeishuDocAPI
from feishu_converter.converter import FeishuConverter
from feishu_converter.adapters.markdown_adapter import MarkdownAdapter

# 初始化API
api = FeishuDocAPI()

# 获取文档信息
document_info = api.get_document_info("your_document_token")

# 转换为Markdown
converter = FeishuConverter()
adapter = MarkdownAdapter()
markdown_result = converter.convert(api, "your_document_token", adapter)
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

## 依赖

- requests
- fastmcp (用于MCP服务)
- python-dotenv (如果使用.env文件)