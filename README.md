# 飞书文档转换器

这是一个功能强大的飞书文档转换项目，可以将飞书文档转换为多种格式，包括 Markdown 和 PDF。该项目还提供了批量转换、文档创建等工具，以及 MCP（Model Context Protocol）服务，便于 AI 模型与飞书文档进行交互。

## 功能

- **文档转换**：将飞书文档转换为 Markdown 和 PDF 格式
- **批量转换**：从 JSON 文件批量转换多个文档
- **文档创建**：创建包含 50+ 种块类型的 Demo 文档用于测试
- **命令行工具**：提供便捷的命令行接口
- **MCP 服务**：通过标准化接口与飞书文档交互
- **支持 50+ 块类型**：包括文本、标题、列表、代码、表格、引用、待办事项、高亮块等

## 安装

### 快速开始

```bash
# 1. 克隆项目
# 2. 进入项目目录
# 3. 运行启动脚本
./start.sh setup
```

### 手动安装

```bash
# 安装依赖
pip install -r requirements.txt

# 创建虚拟环境（可选）
python3 -m venv venv
source venv/bin/activate
```

## 配置

在使用前，请确保设置了以下环境变量：

```bash
export FEISHU_APP_ID=your_app_id
export FEISHU_APP_SECRET=your_app_secret
```

或者在 `.env` 文件中设置这些变量（可从 `.env.example` 复制）：

```bash
cp .env.example .env
# 编辑 .env 文件，添加你的凭证
```

## 使用

### 命令行工具

#### 1. 单文档转换

```bash
# 转换为 Markdown
./start.sh convert https://xxx.feishu.cn/docx/xxx

# 转换为 PDF
./start.sh convert https://xxx.feishu.cn/docx/xxx pdf
```

#### 2. 批量转换

```bash
# 从 JSON 文件批量转换
./start.sh batch get_info.json ./output markdown

# 批量转换为 PDF
./start.sh batch get_info.json ./output pdf
```

#### 3. 创建 Demo 文档

```bash
# 创建基础 Demo 文档
./start.sh demo

# 创建完整 Demo 文档（50+ 块类型）
./start.sh demo --comprehensive
```

#### 4. 完整测试

```bash
# 创建 + 转换 + 比对
./start.sh compare
```

### Python API

```python
from feishu_converter.api import FeishuDocAPI
from feishu_converter.converter import FeishuConverter

# 初始化转换器
converter = FeishuConverter()

# 转换文档
converter.convert(
    "https://xxx.feishu.cn/docx/xxx",
    "markdown",
    "./output.md"
)

# 批量转换
from feishu_converter.tools import BatchConverter

batch_converter = BatchConverter()
batch_converter.convert_from_json_file(
    "get_info.json",
    "./output",
    "markdown"
)

# 创建 Demo 文档
from feishu_converter.tools import create_comprehensive_demo_document
doc_token = create_comprehensive_demo_document()
print(f"Demo 文档创建成功: {doc_token}")
```

## 工具模块

### 1. 批量转换器 (BatchConverter)

- **功能**：从 JSON 文件批量转换多个飞书文档
- **特点**：
  - 支持自定义请求间隔，避免 API 速率限制
  - 默认使用文档标题作为文件名
  - 生成转换报告

### 2. 文档创建器 (DocumentCreator)

- **功能**：创建包含多种块类型的 Demo 文档
- **用途**：用于测试转换功能的完整性
- **支持通过API创建的块类型**：
  - 基础块：文本、标题（1-9级）、列表、代码、引用
  - 高级块：表格、分割线、高亮块、待办事项

- **不支持通过API创建的块类型**：
  - 媒体块：图片、文件、思维笔记、画板
  - 嵌入块：电子表格、多维表格、内嵌网页
  - 其他块：流程图、会话卡片、OKR、Jira问题、Wiki目录、议程块、链接预览、开放平台小组件、视图块、引用容器、同步块、AI模板

## MCP 服务

本项目包含一个 MCP（Model Context Protocol）服务，允许 AI 模型通过标准化接口与飞书文档进行交互。

### 启动 MCP 服务

```bash
# 使用启动脚本
./mcp/start.sh

# 或者直接运行 Python 文件
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

## 支持的块类型

项目支持以下 50+ 种飞书文档块类型：

| 类型 | 描述 | 支持状态 |
|------|------|----------|
| 1 | 页面 (Page) | ✅ |
| 2 | 文本 (Text) | ✅ |
| 3-11 | 标题 (Heading 1-9) | ✅ |
| 12 | 无序列表 (Bullet) | ✅ |
| 13 | 有序列表 (Ordered) | ✅ |
| 14 | 代码块 (Code) | ✅ |
| 15 | 引用 (Quote) | ✅ |
| 16 | 待办事项 (Todo) | ✅ |
| 17 | 多维表格 (Bitable) | ✅ |
| 18 | 高亮块 (Callout) | ✅ |
| 19 | 会话卡片 (ChatCard) | ✅ |
| 20 | 流程图 & UML (Diagram) | ✅ |
| 21 | 分割线 (Divider) | ✅ |
| 22 | 文件 (File) | ✅ |
| 23 | 分栏 (Grid) | ✅ |
| 24 | 分栏列 (GridColumn) | ✅ |
| 25 | 内嵌 Block (Iframe) | ✅ |
| 26 | 图片 (Image) | ✅ |
| 27 | 开放平台小组件 (ISV) | ✅ |
| 28 | 思维笔记 (Mindnote) | ✅ |
| 29 | 电子表格 (Sheet) | ✅ |
| 30 | 表格 (Table) | ✅ |
| 31 | 表格单元格 (TableCell) | ✅ |
| 32 | 视图 (View) | ✅ |
| 33 | 引用容器 (QuoteContainer) | ✅ |
| 34 | 任务 (Task) | ✅ |
| 35-38 | OKR 相关块 | ✅ |
| 39 | 新版文档小组件 (AddOns) | ✅ |
| 40 | Jira 问题 (JiraIssue) | ✅ |
| 41 | Wiki 目录 (WikiCatalog) | ✅ |
| 42 | 画板 (Board) | ✅ |
| 43 | 议程 (Agenda) | ✅ |
| 44 | 议程项 (AgendaItem) | ✅ |
| 45 | 议程项标题 (AgendaItemTitle) | ✅ |
| 46 | 议程项内容 (AgendaItemContent) | ✅ |
| 47 | 链接预览 (LinkPreview) | ✅ |
| 48 | 源同步块 (SourceSynced) | ✅ |
| 49 | 引用同步块 (ReferenceSynced) | ✅ |
| 50 | 子页面列表 (SubPageList) | ✅ |
| 51 | AI 模板 (AITemplate) | ✅ |
| 999 | 未支持 (Undefined) | ✅ |

## 项目结构

```
feishu_helper/
├── feishu_converter/          # 核心转换模块
│   ├── adapters/              # 格式适配器（Markdown、PDF）
│   ├── demo/                  # 示例和测试
│   ├── entities/              # 数据实体
│   ├── enums/                 # 枚举类型
│   ├── fetchers/              # 文档获取器
│   ├── process/               # 块处理器
│   ├── tools/                 # 工具模块
│   │   ├── batch_converter.py  # 批量转换器
│   │   └── document_creator.py # 文档创建器
│   ├── utils/                 # 工具函数
│   ├── api.py                 # 飞书 API 封装
│   ├── converter.py           # 转换器核心
│   ├── interfaces.py          # 接口定义
│   └── utils.py               # 通用工具
├── mcp/                       # MCP 服务
├── output/                    # 输出目录
├── .env.example               # 环境变量示例
├── main.py                    # 主命令行入口
├── batch_convert.py           # 批量转换脚本
├── start.sh                   # 启动脚本
└── requirements.txt           # 依赖配置
```

## 依赖

- `requests` - HTTP 请求
- `fastmcp` - MCP 服务
- `reportlab` - PDF 生成
- `python-dotenv` - 环境变量管理
- `Pillow` - 图像处理
- `tqdm` - 进度条
- `lark-oapi` - 飞书 API SDK

## 扩展性

本项目设计具有良好的扩展性：

1. **添加新的输出格式**：实现 `IFormatAdapter` 接口
2. **扩展 API 功能**：通过 `FeishuDocAPI` 类
3. **添加新的文档获取方式**：实现 `IDocumentFetcher` 接口
4. **支持新的块类型**：在 `process` 目录中添加相应的处理器

## 许可证

MIT License
