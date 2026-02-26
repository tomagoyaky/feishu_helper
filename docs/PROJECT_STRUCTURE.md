# 飞书文档转换器项目结构

## 项目概述

这是一个基于飞书开放平台API的文档转换工具，可以从飞书文档链接直接转换为PDF和Markdown格式。

## 目录结构

```
feishu_helper/
├── main.py                     # 项目入口文件
├── PROJECT_README.md          # 项目详细说明
├── USAGE.md                   # 使用说明
├── PROJECT_STRUCTURE.md       # 本文件，项目结构说明
├── requirements.txt           # 项目依赖
├── .env                       # 环境变量配置（本地开发）
├── .gitignore                 # Git忽略文件配置
├── workspace/                 # 输出工作目录
├── test_functionality.py      # 功能测试脚本
├── feishu_converter/          # 核心转换器包
│   ├── __init__.py           # 包初始化
│   ├── converter.py          # 主转换器类
│   ├── interfaces.py         # 接口定义
│   ├── api.py               # 飞书API客户端
│   ├── utils.py             # 工具函数
│   ├── fetchers/            # 文档获取器
│   │   └── document_fetcher.py  # 飞书文档获取器
│   ├── adapters/            # 格式转换适配器
│   │   ├── pdf_adapter.py   # PDF转换适配器
│   │   └── markdown_adapter.py  # Markdown转换适配器
│   ├── entities/            # 数据实体定义
│   │   ├── __init__.py      # 实体模块初始化
│   │   ├── block.py         # 块实体基类
│   │   ├── text_elements.py # 文本元素实体
│   │   ├── agenda.py        # 议程块实体
│   │   ├── agenda_item.py   # 议程项块实体
│   │   ├── agenda_item_title.py  # 议程项标题块实体
│   │   ├── agenda_item_content.py  # 议程项内容块实体
│   │   ├── aitemplate.py    # AI模板块实体
│   │   ├── bitable.py       # 多维表格块实体
│   │   ├── board.py         # 画板块实体
│   │   ├── callout.py       # 高亮块实体
│   │   ├── chat_card.py     # 会话卡片块实体
│   │   ├── diagram.py       # 流程图块实体
│   │   ├── divider.py       # 分割线块实体
│   │   ├── file_block.py    # 文件块实体
│   │   ├── grid.py          # 分栏块实体
│   │   ├── grid_column.py   # 分栏列块实体
│   │   ├── iframe.py        # 内嵌块实体
│   │   ├── image.py         # 图片块实体
│   │   ├── isv.py           # 开放平台小组件块实体
│   │   ├── jira_issue.py    # Jira问题块实体
│   │   ├── link_preview.py  # 链接预览块实体
│   │   ├── mindnote.py      # 思维笔记块实体
│   │   ├── okr.py           # OKR相关实体
│   │   ├── quote_container.py  # 引用容器块实体
│   │   ├── task.py          # 任务块实体
│   │   ├── view.py          # 视图块实体
│   │   ├── wiki_catalog.py  # Wiki目录块实体
│   │   ├── sheet.py         # 电子表格块实体
│   │   ├── table.py         # 表格块实体
│   │   ├── table_cell.py    # 单元格块实体
│   │   ├── source_synced.py # 源同步块实体
│   │   ├── reference_synced.py  # 引用同步块实体
│   │   ├── sub_page_list.py # Wiki新版子目录块实体
│   │   └── ...              # 其他块实体
│   └── enums/               # 枚举类型定义
│       └── __init__.py      # 所有枚举类型定义
```

## 核心模块说明

### 1. api.py
- 封装飞书开放平台的API调用
- 实现获取访问令牌、文档信息、文档块内容等功能
- 处理API请求和响应

### 2. fetchers/document_fetcher.py
- 实现IDocumentFetcher接口
- 负责从飞书API获取文档内容
- 包含获取文档内容、纯文本内容和文档信息的方法

### 3. adapters/
- 格式转换适配器，实现IFormatAdapter接口
- pdf_adapter.py: 将文档内容转换为PDF格式
- markdown_adapter.py: 将文档内容转换为Markdown格式

### 4. entities/
- 定义所有文档块的实体类
- 每个实体类对应飞书文档中的一种块类型
- 使用dataclass实现，支持类型安全和易用性

### 5. enums/
- 定义所有相关的枚举类型
- 包括对齐方式、块类型、视图类型、颜色等枚举

### 6. converter.py
- 主转换器类FeishuConverter
- 协调文档获取和格式转换过程
- 实现IFeishuConverter接口

## 工作流程

1. 用户提供飞书文档链接
2. 转换器初始化API客户端和获取器
3. 通过API获取文档信息和内容
4. 根据输出格式选择对应的适配器
5. 适配器将文档内容转换为指定格式
6. 保存转换后的文件到指定路径

## 设计模式

- 适配器模式：不同格式转换器实现统一接口
- 策略模式：根据不同输出格式选择不同处理策略
- 工厂模式：根据格式类型创建对应的适配器

## 扩展性

- 可以通过添加新的适配器来支持更多输出格式
- 可以通过扩展实体类来支持更多文档块类型
- 接口设计便于单元测试和模块替换