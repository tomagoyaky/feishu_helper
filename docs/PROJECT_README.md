# 飞书文档转换器

这是一个基于飞书开放平台API的文档转换工具，可以从飞书文档链接直接转换为PDF和Markdown格式。

## 功能特性

- 从飞书文档链接获取文档内容
- 支持转换为PDF格式
- 支持转换为Markdown格式
- 支持多种文档元素：标题、列表、引用、代码块、表格、图片等

## 技术架构

项目采用了清晰的架构设计：

- `api/`: 封装飞书API调用
- `fetchers/`: 文档内容获取器
- `adapters/`: 格式转换适配器
- `entities/`: 数据实体定义
- `enums/`: 枚举类型定义
- `interfaces/`: 接口定义

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置

在使用前，需要在 `.env` 文件中配置飞书应用的凭据：

```env
FEISHU_APP_ID=your_app_id
FEISHU_APP_SECRET=your_app_secret
WORKSPACE=/path/to/workspace
```

## 使用方法

### 命令行使用

```bash
python main.py <飞书文档链接> <输出格式> <输出路径>
```

示例：

```bash
# 转换为PDF
python main.py https://example.feishu.cn/docx/xxx pdf ./output.pdf

# 转换为Markdown
python main.py https://example.feishu.cn/docx/xxx markdown ./output.md
```

### 脚本使用

```python
from feishu_converter import FeishuConverter

converter = FeishuConverter(app_id="your_app_id", app_secret="your_app_secret")
converter.convert("https://example.feishu.cn/docx/xxx", "pdf", "./output.pdf")
```

## 支持的文档元素

- [x] 页面和标题
- [x] 普通文本
- [x] 无序和有序列表
- [x] 代码块
- [x] 引用
- [x] 待办事项
- [x] 分割线
- [x] 表格
- [x] 图片（占位符）
- [x] 高亮块

## API接口说明

### 获取文档信息
- 对应API: `GET /open-apis/docx/v1/documents/:document_id`
- 获取文档的基本信息，如标题、版本等

### 获取文档块内容
- 对应API: `GET /open-apis/docx/v1/documents/:document_id/blocks`
- 获取文档的所有块内容，支持分页

### 获取文档纯文本内容
- 对应API: `GET /open-apis/docx/v1/documents/:document_id/raw_content`
- 获取文档的纯文本内容

## 项目结构

```
feishu_converter/
├── api/                 # API客户端
│   └── api.py          # 飞书API实现
├── fetchers/           # 文档获取器
│   └── document_fetcher.py  # 文档获取实现
├── adapters/           # 格式适配器
│   ├── pdf_adapter.py  # PDF转换适配器
│   └── markdown_adapter.py  # Markdown转换适配器
├── entities/           # 数据实体
│   ├── __init__.py
│   ├── block.py        # 块实体
│   ├── text_elements.py # 文本元素实体
│   └── ...             # 其他实体文件
├── enums/              # 枚举定义
│   └── __init__.py
├── interfaces.py       # 接口定义
├── utils.py            # 工具函数
└── converter.py        # 主转换器
```

## 注意事项

1. 需要为应用配置适当的文档权限
2. API调用频率有限制，请避免过于频繁的请求
3. 图片内容在转换时会保留为占位符，如需完整图片内容需要额外处理
4. 表格在PDF和Markdown中的显示可能略有差异