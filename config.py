"""
项目配置文件
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 飞书API配置
FEISHU_APP_ID = os.getenv('FEISHU_APP_ID', '')
FEISHU_APP_SECRET = os.getenv('FEISHU_APP_SECRET', '')

# 工作空间配置
WORKSPACE = os.getenv('WORKSPACE', '/Users/neolix/Documents/vscode/feishu_helper/workspace')

# API基础URL
BASE_URL = "https://open.feishu.cn/open-apis"

# 支持的输出格式
SUPPORTED_FORMATS = {
    'pdf': 'PDF格式',
    'markdown': 'Markdown格式'
}

# 默认请求超时时间（秒）
DEFAULT_TIMEOUT = 30

# 最大重试次数
MAX_RETRIES = 3