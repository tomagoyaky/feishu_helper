# 飞书文档转换器使用说明

这是一个可以从飞书文档链接直接转换为PDF和Markdown格式的工具。

## 环境准备

1. 确保已安装Python 3.8+环境
2. 安装依赖：`pip install -r requirements.txt`

## 配置

在`.env`文件中配置以下环境变量：

```
FEISHU_APP_ID=your_app_id
FEISHU_APP_SECRET=your_app_secret
WORKSPACE=./workspace
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

### 编程使用

```python
from feishu_converter import FeishuConverter

converter = FeishuConverter(app_id="your_app_id", app_secret="your_app_secret")
success = converter.convert("https://example.feishu.cn/docx/xxx", "pdf", "./output.pdf")
print(f"转换{'成功' if success else '失败'}")
```

## 支持的输出格式

- `pdf` - 转换为PDF格式
- `markdown` - 转换为Markdown格式

## 注意事项

1. 需要为飞书应用配置适当的文档权限
2. 转换过程中会打印API请求信息，便于调试
3. 输出路径会自动创建必要的目录
4. 飞书文档链接支持docx、docs、wiki三种格式

## API接口说明

项目使用飞书开放平台的以下API：

- `/open-apis/auth/v3/tenant_access_token/internal` - 获取访问令牌
- `/open-apis/docx/v1/documents/:document_id` - 获取文档信息
- `/open-apis/docx/v1/documents/:document_id/blocks` - 获取文档块内容
- `/open-apis/docx/v1/documents/:document_id/raw_content` - 获取文档纯文本内容