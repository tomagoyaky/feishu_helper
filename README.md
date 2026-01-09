# 飞书文档格式转换工具

飞书文档格式转换工具是一个将飞书文档链接转换为多种格式（PDF、Markdown等）的Python项目。该项目采用分层设计，支持扩展到更多文档格式转换。

## 功能特性

- 将飞书文档链接转换为PDF格式
- 将飞书文档链接转换为Markdown格式
- 扩展性强，易于添加新的输出格式
- 模块化设计，便于维护
- 基于官方API实现，符合飞书API规范

## 架构设计

项目采用分层架构设计：

- **接口层**: 提供统一的转换接口
- **业务逻辑层**: 处理文档转换逻辑
- **API层**: 实现飞书官方API接口
- **数据访问层**: 负责与飞书API交互
- **适配器层**: 负责不同格式的转换实现

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