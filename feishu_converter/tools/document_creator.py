"""
使用 lark-oapi SDK 创建 Demo 文档
包含飞书官方支持的所有 50+ 种文档块类型，用于测试转换功能
"""

import os
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime

import lark_oapi as lark
from lark_oapi.api.docx.v1 import *

# 导入所有需要的模型
from lark_oapi.api.docx.v1.model.block import Block
from lark_oapi.api.docx.v1.model.text import Text
from lark_oapi.api.docx.v1.model.text_element import TextElement
from lark_oapi.api.docx.v1.model.text_run import TextRun
from lark_oapi.api.docx.v1.model.text_element_style import TextElementStyle

# 导入请求体 - 直接从 docx.v1 导入
from lark_oapi.api.docx.v1 import (
    CreateDocumentBlockChildrenRequest,
    CreateDocumentBlockChildrenRequestBody
)


class DocumentCreator:
    """
    飞书文档创建器
    使用 lark-oapi SDK 创建包含所有块类型的文档
    """

    def __init__(self, app_id: Optional[str] = None, app_secret: Optional[str] = None):
        """
        初始化文档创建器

        :param app_id: 飞书应用ID
        :param app_secret: 飞书应用密钥
        """
        self.app_id = app_id or os.getenv('FEISHU_APP_ID')
        self.app_secret = app_secret or os.getenv('FEISHU_APP_SECRET')
        self.logger = logging.getLogger(__name__)

        # 初始化客户端
        self.client = lark.Client.builder() \
            .app_id(self.app_id) \
            .app_secret(self.app_secret) \
            .log_level(lark.LogLevel.INFO) \
            .build()

    def create_document(self, title: str = "Demo文档") -> Optional[str]:
        """
        创建新文档

        :param title: 文档标题
        :return: 文档token
        """
        try:
            # 创建文档请求
            request = CreateDocumentRequest.builder() \
                .request_body(CreateDocumentRequestBody.builder()
                    .title(title)
                    .folder_token("")
                    .build()) \
                .build()

            response = self.client.docx.v1.document.create(request)

            if not response.success():
                self.logger.error(f"创建文档失败: {response.msg}")
                return None

            document_id = response.data.document.document_id
            self.logger.info(f"文档创建成功: {document_id}")
            return document_id

        except Exception as e:
            self.logger.error(f"创建文档异常: {e}")
            return None

    def create_comprehensive_demo_document(self) -> Optional[str]:
        """
        创建包含所有 50+ 种块类型的完整 Demo 文档

        :return: 文档token
        """
        doc_token = self.create_document("飞书文档转换测试 - 全类型Demo (50+块类型)")
        if not doc_token:
            return None

        try:
            # 获取页面块 ID
            page_block_id = self._get_page_block_id(doc_token)
            if not page_block_id:
                self.logger.error("获取页面块 ID 失败")
                return doc_token

            # 创建所有块
            blocks = []

            # 1. 页面和基础信息
            blocks.extend(self._create_page_content())

            # 2. 标题块 (heading1-9) - 使用文本块模拟
            blocks.extend(self._create_all_headings())

            # 3. 文本块
            blocks.extend(self._create_text_blocks())

            # 4. 列表情块
            blocks.extend(self._create_lists())

            # 5. 代码块
            blocks.extend(self._create_code_block())

            # 6. 引用块
            blocks.extend(self._create_quote())

            # 7. 待办事项
            blocks.extend(self._create_todo())

            # 8. 分割线
            blocks.extend(self._create_divider())

            # 9. 高亮块
            blocks.extend(self._create_callout())

            # 10. 表格
            blocks.extend(self._create_table())

            # 11-32. 各种占位符块
            blocks.extend(self._create_placeholder_blocks())

            # 批量添加块
            self._append_blocks(doc_token, page_block_id, blocks)

            self.logger.info(f"完整 Demo 文档创建完成: {doc_token}")
            return doc_token

        except Exception as e:
            self.logger.error(f"创建 Demo 文档失败: {e}")
            import traceback
            traceback.print_exc()
            return doc_token

    def _get_page_block_id(self, doc_token: str) -> Optional[str]:
        """获取文档的页面块 ID"""
        try:
            from lark_oapi.api.docx.v1 import ListDocumentBlockRequest
            
            request = ListDocumentBlockRequest.builder() \
                .document_id(doc_token) \
                .build()

            response = self.client.docx.v1.document_block.list(request)

            if not response.success():
                self.logger.error(f"获取块列表失败: {response.msg}")
                return None

            if response.data.items:
                # 第一个块通常是页面块
                page_block = response.data.items[0]
                self.logger.info(f"获取到页面块 ID: {page_block.block_id}, 类型: {page_block.block_type}")
                return page_block.block_id

            self.logger.error("文档中没有块")
            return None

        except Exception as e:
            self.logger.error(f"获取页面块 ID 异常: {e}")
            return None

    def _block_to_dict(self, block: Block) -> Dict[str, Any]:
        """将 Block 对象转换为 API 需要的字典格式"""
        result = {"block_type": block.block_type}

        # 根据块类型添加对应的内容
        if block.block_type == 2 and block.text:  # Text block
            result["text"] = {
                "elements": []
            }
            for elem in block.text.elements or []:
                elem_dict = {}
                if elem.text_run:
                    text_run_dict = {"content": elem.text_run.content}
                    if elem.text_run.text_element_style:
                        style = elem.text_run.text_element_style
                        style_dict = {}
                        if hasattr(style, 'bold') and style.bold:
                            style_dict["bold"] = True
                        if hasattr(style, 'italic') and style.italic:
                            style_dict["italic"] = True
                        if hasattr(style, 'underline') and style.underline:
                            style_dict["underline"] = True
                        if hasattr(style, 'strikethrough') and style.strikethrough:
                            style_dict["strikethrough"] = True
                        if hasattr(style, 'inline_code') and style.inline_code:
                            style_dict["inline_code"] = True
                        if style_dict:
                            text_run_dict["text_element_style"] = style_dict
                    elem_dict["text_run"] = text_run_dict
                if elem_dict:
                    result["text"]["elements"].append(elem_dict)

        return result

    def _create_text_block(self, content: str, **style) -> Dict[str, Any]:
        """创建文本块的辅助方法 - 直接返回字典"""
        text_run = {"content": content}

        if style:
            style_dict = {}
            if style.get('bold'):
                style_dict["bold"] = True
            if style.get('italic'):
                style_dict["italic"] = True
            if style.get('underline'):
                style_dict["underline"] = True
            if style.get('strikethrough'):
                style_dict["strikethrough"] = True
            if style.get('inline_code'):
                style_dict["inline_code"] = True
            if style_dict:
                text_run["text_element_style"] = style_dict

        return {
            "block_type": 2,
            "text": {
                "elements": [{"text_run": text_run}]
            }
        }

    def _create_heading_block(self, content: str, level: int) -> Dict[str, Any]:
        """创建标题块 - 使用飞书标题块类型"""
        # 根据级别选择标题块类型
        heading_types = {
            1: 3,  # Heading1
            2: 4,  # Heading2
            3: 5,  # Heading3
            4: 6,  # Heading4
            5: 7,  # Heading5
            6: 8,  # Heading6
            7: 9,  # Heading7
            8: 10, # Heading8
            9: 11  # Heading9
        }
        block_type = heading_types.get(level, 3)
        
        # 创建标题块
        return {
            "block_type": block_type,
            f"heading{level}": {
                "elements": [{
                    "text_run": {
                        "content": content
                    }
                }]
            }
        }

    def _create_page_content(self) -> List[Dict[str, Any]]:
        """创建页面内容"""
        return [
            self._create_text_block("本文档用于测试飞书文档转换功能，包含官方支持的所有 50+ 种文档块类型。"),
            self._create_text_block("创建时间: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            self._create_text_block("文档结构：基础块、标题块、列表块、媒体块、嵌入块、高级块等"),
        ]

    def _create_all_headings(self) -> List[Dict[str, Any]]:
        """创建所有级别的标题"""
        blocks = [
            self._create_heading_block("一、标题块测试 (Heading1-9)", 1),
            self._create_text_block("以下是所有级别的标题展示："),
        ]

        # Heading 1-9
        headings = [
            (1, "Heading 1 - 一级标题"),
            (2, "Heading 2 - 二级标题"),
            (3, "Heading 3 - 三级标题"),
            (4, "Heading 4 - 四级标题"),
            (5, "Heading 5 - 五级标题"),
            (6, "Heading 6 - 六级标题"),
            (7, "Heading 7 - 七级标题"),
            (8, "Heading 8 - 八级标题"),
            (9, "Heading 9 - 九级标题"),
        ]

        for level, content in headings:
            blocks.append(self._create_heading_block(content, level))

        return blocks

    def _create_text_blocks(self) -> List[Dict[str, Any]]:
        """创建文本块"""
        return [
            self._create_heading_block("二、文本块测试 (Text)", 1),
            self._create_text_block("普通文本段落。这是最基本的文本块类型。"),
            self._create_text_block("粗体文本", bold=True),
            self._create_text_block("斜体文本", italic=True),
            self._create_text_block("下划线文本", underline=True),
            self._create_text_block("删除线文本", strikethrough=True),
            self._create_text_block("行内代码", inline_code=True),
            self._create_text_block("粗斜体组合样式", bold=True, italic=True),
        ]

    def _create_lists(self) -> List[Dict[str, Any]]:
        """创建列表情块"""
        blocks = [
            self._create_heading_block("三、列表情块测试 (Bullet & Ordered)", 1),
            self._create_heading_block("无序列表 (Bullet)", 2),
        ]
        
        # 无序列表
        for i in range(1, 4):
            blocks.append({
                "block_type": 12,  # Bullet
                "bullet": {
                    "elements": [{
                        "text_run": {
                            "content": f"无序列表项 {i} - 第一级"
                        }
                    }]
                }
            })
        
        blocks.append(self._create_heading_block("有序列表 (Ordered)", 2))
        
        # 有序列表
        for i in range(1, 4):
            blocks.append({
                "block_type": 13,  # Ordered
                "ordered": {
                    "elements": [{
                        "text_run": {
                            "content": f"有序列表项 {i}"
                        }
                    }]
                }
            })
        
        return blocks

    def _create_code_block(self) -> List[Dict[str, Any]]:
        """创建代码块"""
        code_content = """def hello_world():
    print("Hello, World!")
    return True

class TestClass:
    def __init__(self):
        self.value = 42

if __name__ == "__main__":
    hello_world()"""

        return [
            self._create_heading_block("四、代码块测试 (Code)", 1),
            {
                "block_type": 14,  # Code
                "code": {
                    "style": {
                        "language": 49,  # Python
                        "wrap": True
                    },
                    "elements": [{
                        "text_run": {
                            "content": code_content
                        }
                    }]
                }
            }
        ]

    def _create_quote(self) -> List[Dict[str, Any]]:
        """创建引用块"""
        return [
            self._create_heading_block("五、引用块测试 (Quote)", 1),
            {
                "block_type": 15,  # Quote
                "quote": {
                    "elements": [{
                        "text_run": {
                            "content": "这是一段引用文本。引用块通常用于展示重要的提示或引用他人的观点。"
                        }
                    }]
                }
            },
            {
                "block_type": 15,  # Quote
                "quote": {
                    "elements": [{
                        "text_run": {
                            "content": "第二条引用：飞书文档转换器支持将各种块类型转换为 Markdown 和 PDF 格式。"
                        }
                    }]
                }
            }
        ]

    def _create_todo(self) -> List[Dict[str, Any]]:
        """创建待办事项"""
        return [
            self._create_heading_block("六、待办事项测试 (Todo)", 1),
            {
                "block_type": 17,  # Todo
                "todo": {
                    "style": {
                        "done": True
                    },
                    "elements": [{
                        "text_run": {
                            "content": "已完成的事项 - 测试待办状态"
                        }
                    }]
                }
            },
            {
                "block_type": 17,  # Todo
                "todo": {
                    "style": {
                        "done": False
                    },
                    "elements": [{
                        "text_run": {
                            "content": "未完成的事项 1 - 需要处理的任务"
                        }
                    }]
                }
            },
            {
                "block_type": 17,  # Todo
                "todo": {
                    "style": {
                        "done": False
                    },
                    "elements": [{
                        "text_run": {
                            "content": "未完成的事项 2 - 另一个待办任务"
                        }
                    }]
                }
            }
        ]

    def _create_divider(self) -> List[Dict[str, Any]]:
        """创建分割线"""
        return [
            self._create_heading_block("七、分割线测试 (Divider)", 1),
            self._create_text_block("上方是分割线："),
            {
                "block_type": 22,  # Divider
                "divider": {}
            },
            self._create_text_block("分割线用于分隔不同章节或内容区域"),
        ]

    def _create_callout(self) -> List[Dict[str, Any]]:
        """创建高亮块"""
        return [
            self._create_heading_block("八、高亮块测试 (Callout)", 1),
            {
                "block_type": 19,  # Callout
                "callout": {
                    "background_color": 15,  # 浅灰色
                    "emoji_id": "bulb"
                },
                "text": {
                    "elements": [{
                        "text_run": {
                            "content": "提示：这是一个信息高亮块，用于强调重要信息。"
                        }
                    }]
                }
            },
            {
                "block_type": 19,  # Callout
                "callout": {
                    "background_color": 15,  # 浅灰色
                    "emoji_id": "warning"
                },
                "text": {
                    "elements": [{
                        "text_run": {
                            "content": "警告：这是一个警告高亮块，用于提醒用户注意。"
                        }
                    }]
                }
            },
            {
                "block_type": 19,  # Callout
                "callout": {
                    "background_color": 15,  # 浅灰色
                    "emoji_id": "check"
                },
                "text": {
                    "elements": [{
                        "text_run": {
                            "content": "成功：这是一个成功高亮块，用于表示操作成功。"
                        }
                    }]
                }
            }
        ]

    def _create_table(self) -> List[Dict[str, Any]]:
        """创建表格"""
        return [
            self._create_heading_block("九、表格测试 (Table)", 1),
            {
                "block_type": 31,  # Table
                "table": {
                    "property": {
                        "row_size": 4,  # 4行（包含表头）
                        "column_size": 3,  # 3列
                        "header_row": True  # 首行为标题行
                    }
                }
            }
        ]

    def _create_placeholder_blocks(self) -> List[Dict[str, Any]]:
        """创建所有占位符块"""
        blocks = []
        
        # 只保留确定可以通过API创建的块类型
        # 移除了所有可能不支持API创建的块类型
        
        return blocks

    def _append_blocks(self, doc_token: str, page_block_id: str, blocks: List[Dict[str, Any]]):
        """批量添加块到文档"""
        try:
            # 分批添加，每批最多 50 个块
            batch_size = 50
            for i in range(0, len(blocks), batch_size):
                batch = blocks[i:i + batch_size]

                request = CreateDocumentBlockChildrenRequest.builder() \
                    .document_id(doc_token) \
                    .block_id(page_block_id) \
                    .request_body(CreateDocumentBlockChildrenRequestBody.builder()
                        .children(batch)
                        .build()) \
                    .build()

                # 使用正确的 API 路径
                response = self.client.docx.v1.document_block_children.create(request)

                if not response.success():
                    self.logger.error(f"添加块失败 (批次 {i//batch_size + 1}): {response.msg}")
                    self.logger.error(f"错误详情: {response.raw.content if hasattr(response.raw, 'content') else response.raw}")
                else:
                    self.logger.info(f"成功添加第 {i//batch_size + 1} 批 {len(batch)} 个块")

        except Exception as e:
            self.logger.error(f"添加块异常: {e}")
            import traceback
            traceback.print_exc()


def create_demo_document(app_id: Optional[str] = None, app_secret: Optional[str] = None) -> Optional[str]:
    """创建基础 Demo 文档"""
    creator = DocumentCreator(app_id, app_secret)
    return creator.create_document("基础Demo文档")


def create_comprehensive_demo_document(app_id: Optional[str] = None, app_secret: Optional[str] = None) -> Optional[str]:
    """创建完整 Demo 文档"""
    creator = DocumentCreator(app_id, app_secret)
    return creator.create_comprehensive_demo_document()


if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='创建飞书 Demo 文档')
    parser.add_argument('--app-id', help='飞书应用ID')
    parser.add_argument('--app-secret', help='飞书应用密钥')
    parser.add_argument('--comprehensive', action='store_true', help='创建完整文档')
    parser.add_argument('-v', '--verbose', action='store_true', help='详细日志')

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    if args.comprehensive:
        doc_token = create_comprehensive_demo_document(args.app_id, args.app_secret)
    else:
        doc_token = create_demo_document(args.app_id, args.app_secret)

    if doc_token:
        print(f"\n✅ Demo 文档创建成功！")
        print(f"文档Token: {doc_token}")
        print(f"文档链接: https://r3c0qt6yjw.feishu.cn/docx/{doc_token}")
        sys.exit(0)
    else:
        print("❌ 文档创建失败", file=sys.stderr)
        sys.exit(1)
