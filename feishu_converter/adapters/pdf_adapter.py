"""
PDF适配器
将飞书文档内容转换为PDF格式
"""

import logging
import os
import re
import tempfile
from typing import Dict, Any, Optional
from urllib.parse import urlparse

import requests
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (Image as RLImage, PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

from ..interfaces import IFormatAdapter


class PdfAdapter(IFormatAdapter):
    """
    PDF格式适配器
    负责将飞书文档内容转换为PDF格式
    """

    def __init__(self, download_images: bool = False):
        """
        初始化PDF适配器

        :param download_images: 是否下载图片
        """
        self.logger = logging.getLogger(__name__)
        self.styles = getSampleStyleSheet()
        self.download_images = download_images
        self.temp_dir = None
        self.access_token = None

        # 自定义样式
        self.custom_styles = {
            'Title': ParagraphStyle(
                'Title',
                parent=self.styles['Title'],
                fontSize=24,
                spaceAfter=30,
                spaceBefore=30,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            ),
            'Heading1': ParagraphStyle(
                'Heading1',
                parent=self.styles['Heading1'],
                fontSize=20,
                spaceAfter=20,
                spaceBefore=20,
                fontName='Helvetica-Bold'
            ),
            'Heading2': ParagraphStyle(
                'Heading2',
                parent=self.styles['Heading2'],
                fontSize=18,
                spaceAfter=15,
                spaceBefore=15,
                fontName='Helvetica-Bold'
            ),
            'Heading3': ParagraphStyle(
                'Heading3',
                parent=self.styles['Heading3'],
                fontSize=16,
                spaceAfter=12,
                spaceBefore=12,
                fontName='Helvetica-Bold'
            ),
            'Heading4': ParagraphStyle(
                'Heading4',
                parent=self.styles['Heading4'],
                fontSize=14,
                spaceAfter=10,
                spaceBefore=10,
                fontName='Helvetica-Bold'
            ),
            'Heading5': ParagraphStyle(
                'Heading5',
                parent=self.styles['Heading5'],
                fontSize=13,
                spaceAfter=8,
                spaceBefore=8,
                fontName='Helvetica-Bold'
            ),
            'Heading6': ParagraphStyle(
                'Heading6',
                parent=self.styles['Heading6'],
                fontSize=12,
                spaceAfter=6,
                spaceBefore=6,
                fontName='Helvetica-Bold'
            ),
            'Normal': ParagraphStyle(
                'Normal',
                parent=self.styles['Normal'],
                fontSize=11,
                leading=16,
                spaceAfter=6,
                alignment=TA_JUSTIFY
            ),
            'Code': ParagraphStyle(
                'Code',
                parent=self.styles['Code'],
                fontSize=9,
                leading=12,
                spaceAfter=6,
                leftIndent=20,
                fontName='Courier'
            ),
            'Quote': ParagraphStyle(
                'Quote',
                parent=self.styles['Normal'],
                fontSize=11,
                leftIndent=30,
                rightIndent=30,
                textColor=colors.grey,
                fontName='Helvetica-Oblique'
            ),
            'Bullet': ParagraphStyle(
                'Bullet',
                parent=self.styles['Normal'],
                fontSize=11,
                leftIndent=20,
                bulletIndent=10,
                bulletFontName='Helvetica'
            ),
            'ListItem': ParagraphStyle(
                'ListItem',
                parent=self.styles['Normal'],
                fontSize=11,
                leftIndent=30
            )
        }

    def convert(self, content: Dict[str, Any], output_path: str) -> bool:
        """
        将文档内容转换为PDF格式

        :param content: 飞书文档内容
        :param output_path: 输出路径
        :return: 转换是否成功
        """
        self.logger.info(f"开始将文档内容转换为PDF: {output_path}")

        # 创建临时目录用于存储下载的图片
        if self.download_images:
            self.temp_dir = tempfile.mkdtemp()
            self.logger.debug(f"创建临时目录: {self.temp_dir}")

        try:
            # 创建PDF文档
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            story = []

            # 处理文档内容
            self._process_blocks(content, story)

            # 生成PDF
            doc.build(story)

            self.logger.info(f"PDF转换成功: {output_path}")
            return True
        except Exception as e:
            self.logger.error(f"PDF转换失败: {str(e)}")
            return False
        finally:
            # 清理临时文件
            if self.temp_dir and os.path.exists(self.temp_dir):
                import shutil
                shutil.rmtree(self.temp_dir, ignore_errors=True)
                self.logger.debug(f"清理临时目录: {self.temp_dir}")

    def _process_blocks(self, content: Dict[str, Any], story: list):
        """
        处理文档块内容

        :param content: 文档内容
        :param story: PDF内容列表
        """
        blocks = content.get('items', [])
        block_index = {blk['block_id']: blk for blk in blocks}

        for block in blocks:
            block_type = block.get('block_type')

            # 根据块类型处理内容
            if block_type == 1:  # 页面(Page)
                self._process_page(block, story)
            elif block_type in [3, 4, 5, 6, 7, 8, 9, 10, 11]:  # 标题
                self._process_heading(block, block_type, story)
            elif block_type == 2:  # 文本块
                self._process_text_block(block, story)
            elif block_type == 12:  # 无序列表
                self._process_bullet_list(block, story, block_index)
            elif block_type == 13:  # 有序列表
                self._process_ordered_list(block, story, block_index)
            elif block_type == 14:  # 代码块
                self._process_code(block, story)
            elif block_type == 15:  # 引用
                self._process_quote(block, story)
            elif block_type == 17:  # 待办事项
                self._process_todo(block, story)
            elif block_type == 18:  # 多维表格
                self._process_bitable(block, story)
            elif block_type == 19:  # 高亮块
                self._process_callout(block, story)
            elif block_type == 22:  # 分割线
                self._process_divider(story)
            elif block_type == 27:  # 图片
                self._process_image(block, story)
            elif block_type == 31:  # 表格
                self._process_table(block, story, block_index)
            elif block_type == 30:  # 电子表格
                self._process_sheet(block, story)
            elif block_type == 43:  # 画板
                self._process_board(block, story)
            elif block_type == 44:  # 议程
                self._process_agenda(block, story)
            elif block_type in [20, 21, 23, 24, 25, 26, 28, 29, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 45, 46, 47, 48, 49, 50, 51, 52, 999]:
                # 其他块类型，添加占位符
                self._process_placeholder(block, block_type, story)

    def _extract_text_content(self, elements: list) -> str:
        """从元素中提取文本内容，支持样式"""
        text_parts = []
        for element in elements:
            if 'text_run' in element:
                text_run = element['text_run']
                content = text_run.get('content', '')
                style = text_run.get('text_element_style', {})

                if style:
                    # 处理样式
                    bold = style.get('bold', False)
                    italic = style.get('italic', False)
                    underline = style.get('underline', False)
                    strikethrough = style.get('strikethrough', False)
                    inline_code = style.get('inline_code', False)

                    # 转义HTML特殊字符
                    content = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

                    # 应用样式
                    if inline_code:
                        content = f"<code>{content}</code>"
                    if bold:
                        content = f"<b>{content}</b>"
                    if italic:
                        content = f"<i>{content}</i>"
                    if underline:
                        content = f"<u>{content}</u>"
                    if strikethrough:
                        content = f"<strike>{content}</strike>"

                text_parts.append(content)
            elif 'mention_user' in element:
                user_id = element['mention_user'].get('user_id', '')
                text_parts.append(f"@{user_id}")
            elif 'mention_doc' in element:
                doc_token = element['mention_doc'].get('token', '')
                text_parts.append(f"[文档:{doc_token}]")

        return ''.join(text_parts)

    def _process_page(self, block: Dict[str, Any], story: list):
        """处理页面块"""
        page_data = block.get('page', {})
        elements = page_data.get('elements', [])

        if elements:
            content = self._extract_text_content(elements)
            if content:
                story.append(Paragraph(content, self.custom_styles['Title']))
                story.append(Spacer(1, 12))

    def _process_heading(self, block: Dict[str, Any], block_type: int, story: list):
        """处理标题块"""
        heading_key = f'heading{block_type - 2}'
        heading_data = block.get(heading_key, {})
        elements = heading_data.get('elements', [])

        if elements:
            content = self._extract_text_content(elements)
            if content:
                style_name = f'Heading{block_type - 2}'
                style = self.custom_styles.get(style_name, self.custom_styles['Heading1'])
                story.append(Paragraph(content, style))
                story.append(Spacer(1, 6))

    def _process_text_block(self, block: Dict[str, Any], story: list):
        """处理文本块"""
        text_data = block.get('text', {})
        elements = text_data.get('elements', [])

        if elements:
            content = self._extract_text_content(elements)
            if content:
                story.append(Paragraph(content, self.custom_styles['Normal']))
                story.append(Spacer(1, 6))

    def _process_bullet_list(self, block: Dict[str, Any], story: list, block_index: Dict[str, Any]):
        """处理无序列表"""
        bullet_data = block.get('bullet', {})
        elements = bullet_data.get('elements', [])

        if elements:
            content = self._extract_text_content(elements)
            if content:
                # 使用bullet字符
                bullet_content = f"• {content}"
                story.append(Paragraph(bullet_content, self.custom_styles['Bullet']))

    def _process_ordered_list(self, block: Dict[str, Any], story: list, block_index: Dict[str, Any]):
        """处理有序列表"""
        ordered_data = block.get('ordered', {})
        elements = ordered_data.get('elements', [])

        if elements:
            content = self._extract_text_content(elements)
            if content:
                # 获取序号
                style = ordered_data.get('style', {})
                sequence = style.get('sequence', '1')
                if sequence == 'auto':
                    sequence = '1'

                ordered_content = f"{sequence}. {content}"
                story.append(Paragraph(ordered_content, self.custom_styles['ListItem']))

    def _process_code(self, block: Dict[str, Any], story: list):
        """处理代码块"""
        code_data = block.get('code', {})
        elements = code_data.get('elements', [])
        style = code_data.get('style', {})
        language = style.get('language', 'PlainText')

        if elements:
            content = self._extract_text_content(elements)
            if content:
                # 添加语言标签
                if language and language != 'PlainText':
                    story.append(Paragraph(f"<i>{language}</i>", self.custom_styles['Normal']))

                # 创建代码块背景
                code_text = content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                code_para = Paragraph(f"<font name='Courier' size='9'>{code_text}</font>",
                                      self.custom_styles['Code'])
                story.append(code_para)
                story.append(Spacer(1, 6))

    def _process_quote(self, block: Dict[str, Any], story: list):
        """处理引用块"""
        quote_data = block.get('quote', {})
        elements = quote_data.get('elements', [])

        if elements:
            content = self._extract_text_content(elements)
            if content:
                story.append(Paragraph(f'"{content}"', self.custom_styles['Quote']))
                story.append(Spacer(1, 6))

    def _process_todo(self, block: Dict[str, Any], story: list):
        """处理待办事项"""
        todo_data = block.get('todo', {})
        elements = todo_data.get('elements', [])
        style = todo_data.get('style', {})
        done = style.get('done', False)

        if elements:
            content = self._extract_text_content(elements)
            if content:
                checkbox = '☑' if done else '☐'
                todo_content = f"{checkbox} {content}"
                story.append(Paragraph(todo_content, self.custom_styles['Normal']))
                story.append(Spacer(1, 3))

    def _process_callout(self, block: Dict[str, Any], story: list):
        """处理高亮块"""
        callout_data = block.get('callout', {})
        emoji_id = callout_data.get('emoji_id', '')

        # 获取子块内容
        children = block.get('children', [])
        if children:
            # 简单处理：添加emoji和提示
            story.append(Spacer(1, 6))
            story.append(Paragraph(f"[{emoji_id}] 高亮块", self.custom_styles['Normal']))
            story.append(Spacer(1, 6))

    def _process_divider(self, story: list):
        """处理分割线"""
        story.append(Spacer(1, 12))
        # 创建水平线
        line_data = [['']]
        line_table = Table(line_data, colWidths=[450], rowHeights=[1])
        line_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.grey),
            ('LINEBELOW', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        story.append(line_table)
        story.append(Spacer(1, 12))

    def _process_table(self, block: Dict[str, Any], story: list, block_index: Dict[str, Any]):
        """处理表格"""
        table_data = block.get('table', {})
        cells = table_data.get('cells', [])
        property_data = table_data.get('property', {})
        row_size = property_data.get('row_size', 0)
        column_size = property_data.get('column_size', 0)

        if row_size > 0 and column_size > 0:
            # 构建表格内容
            table_content = []
            for i in range(row_size):
                row = []
                for j in range(column_size):
                    idx = i * column_size + j
                    if idx < len(cells):
                        cell_id = cells[idx]
                        cell_content = self._get_cell_content(cell_id, block_index)
                        row.append(cell_content)
                    else:
                        row.append('')
                table_content.append(row)

            if table_content:
                # 创建表格
                col_width = 450 / column_size
                pdf_table = Table(table_content, colWidths=[col_width] * column_size)

                # 设置表格样式
                table_style = [
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('LEFTPADDING', (0, 0), (-1, -1), 6),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ]

                # 如果有标题行，设置标题样式
                if property_data.get('header_row', False) and row_size > 0:
                    table_style.extend([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ])

                pdf_table.setStyle(TableStyle(table_style))
                story.append(Spacer(1, 6))
                story.append(pdf_table)
                story.append(Spacer(1, 6))

    def _get_cell_content(self, cell_id: str, block_index: Dict[str, Any]) -> str:
        """获取单元格内容"""
        if cell_id not in block_index:
            return str(cell_id)

        cell_block = block_index[cell_id]
        block_type = cell_block.get('block_type')

        if block_type == 32:  # 表格单元格
            # 获取子块
            children = cell_block.get('children', [])
            contents = []
            for child_id in children:
                if child_id in block_index:
                    child_block = block_index[child_id]
                    child_content = self._extract_content_from_block(child_block)
                    if child_content:
                        contents.append(child_content)
            return ' '.join(contents) if contents else ' '

        return self._extract_content_from_block(cell_block)

    def _extract_content_from_block(self, block: Dict[str, Any]) -> str:
        """从块中提取内容"""
        block_type = block.get('block_type')

        if block_type == 2:  # 文本块
            text_data = block.get('text', {})
            elements = text_data.get('elements', [])
            return self._extract_text_content(elements)
        elif block_type in [3, 4, 5, 6, 7, 8, 9, 10, 11]:  # 标题
            level = block_type - 2
            heading_data = block.get(f'heading{level}', {})
            elements = heading_data.get('elements', [])
            return self._extract_text_content(elements)

        return ''

    def _process_image(self, block: Dict[str, Any], story: list):
        """处理图片"""
        image_data = block.get('image', {})
        token = image_data.get('token', '')
        width = image_data.get('width', 100)
        height = image_data.get('height', 100)

        if self.download_images and token:
            # 下载图片
            image_path = self._download_image(token)
            if image_path and os.path.exists(image_path):
                try:
                    # 计算合适的尺寸（最大宽度450pt）
                    max_width = 450
                    aspect_ratio = height / width if width > 0 else 1
                    display_width = min(width, max_width)
                    display_height = display_width * aspect_ratio

                    img = RLImage(image_path, width=display_width, height=display_height)
                    story.append(Spacer(1, 6))
                    story.append(img)
                    story.append(Spacer(1, 6))
                    return
                except Exception as e:
                    self.logger.warning(f"插入图片失败: {e}")

        # 图片占位符
        story.append(Spacer(1, 6))
        story.append(Paragraph(f"[图片: {token[:20]}...]", self.custom_styles['Normal']))
        story.append(Spacer(1, 6))

    def _download_image(self, token: str) -> Optional[str]:
        """下载图片"""
        if not self.access_token:
            return None

        try:
            url = f"https://open.feishu.cn/open-apis/drive/v1/medias/{token}/download"
            headers = {"Authorization": f"Bearer {self.access_token}"}

            response = requests.get(url, headers=headers, stream=True)
            response.raise_for_status()

            # 获取文件扩展名
            content_type = response.headers.get('content-type', '')
            ext = '.jpg'
            if 'png' in content_type:
                ext = '.png'
            elif 'gif' in content_type:
                ext = '.gif'

            # 保存图片
            image_path = os.path.join(self.temp_dir, f"{token}{ext}")
            with open(image_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            return image_path
        except Exception as e:
            self.logger.warning(f"下载图片失败: {e}")
            return None

    def _process_bitable(self, block: Dict[str, Any], story: list):
        """处理多维表格"""
        bitable_data = block.get('bitable', {})
        token = bitable_data.get('token', '')

        story.append(Spacer(1, 6))
        story.append(Paragraph(f"[多维表格: {token[:30]}...]", self.custom_styles['Normal']))
        story.append(Spacer(1, 6))

    def _process_sheet(self, block: Dict[str, Any], story: list):
        """处理电子表格"""
        sheet_data = block.get('sheet', {})
        token = sheet_data.get('token', '')

        story.append(Spacer(1, 6))
        story.append(Paragraph(f"[电子表格: {token[:30]}...]", self.custom_styles['Normal']))
        story.append(Spacer(1, 6))

    def _process_board(self, block: Dict[str, Any], story: list):
        """处理画板"""
        board_data = block.get('board', {})
        token = board_data.get('token', '')

        story.append(Spacer(1, 6))
        story.append(Paragraph(f"[画板: {token[:30]}...]", self.custom_styles['Normal']))
        story.append(Spacer(1, 6))

    def _process_agenda(self, block: Dict[str, Any], story: list):
        """处理议程"""
        story.append(Spacer(1, 6))
        story.append(Paragraph("[议程]", self.custom_styles['Normal']))
        story.append(Spacer(1, 6))

    def _process_placeholder(self, block: Dict[str, Any], block_type: int, story: list):
        """处理其他块类型的占位符"""
        block_type_names = {
            20: "会话卡片",
            21: "流程图/UML",
            23: "文件",
            24: "分栏",
            25: "分栏列",
            26: "内嵌网页",
            28: "开放平台小组件",
            29: "思维笔记",
            33: "视图",
            34: "引用容器",
            35: "任务",
            36: "OKR",
            37: "OKR目标",
            38: "OKR关键结果",
            39: "OKR进展",
            40: "文档小组件",
            41: "Jira问题",
            42: "Wiki目录",
            45: "议程项",
            46: "议程项标题",
            47: "议程项内容",
            48: "链接预览",
            49: "源同步块",
            50: "引用同步块",
            51: "子页面列表",
            52: "AI模板",
            999: "未支持块"
        }

        name = block_type_names.get(block_type, f"块类型{block_type}")
        story.append(Spacer(1, 3))
        story.append(Paragraph(f"[{name}]", self.custom_styles['Normal']))
        story.append(Spacer(1, 3))
