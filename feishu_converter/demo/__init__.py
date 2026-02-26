"""
Demo 文档生成模块
使用 lark-oapi SDK 创建包含各种文档块类型的测试文档
"""

from .document_creator import (
    DocumentCreator,
    create_demo_document,
    create_comprehensive_demo_document
)

__all__ = [
    'DocumentCreator',
    'create_demo_document',
    'create_comprehensive_demo_document'
]
