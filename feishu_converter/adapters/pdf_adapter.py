"""
PDF适配器
将飞书文档内容转换为PDF格式
"""

import logging
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.units import inch
from typing import Dict, Any
from ..interfaces import IFormatAdapter


class PdfAdapter(IFormatAdapter):
    """
    PDF格式适配器
    负责将飞书文档内容转换为PDF格式
    """
    
    def __init__(self):
        """
        初始化PDF适配器
        """
        self.logger = logging.getLogger(__name__)
        self.styles = getSampleStyleSheet()
        
        # 自定义样式
        self.custom_styles = {
            'Heading1': ParagraphStyle(
                'Heading1',
                parent=self.styles['Heading1'],
                fontSize=20,
                spaceAfter=20,
                spaceBefore=20,
                alignment=TA_CENTER
            ),
            'Heading2': ParagraphStyle(
                'Heading2',
                parent=self.styles['Heading2'],
                fontSize=18,
                spaceAfter=15,
                spaceBefore=15
            ),
            'Heading3': ParagraphStyle(
                'Heading3',
                parent=self.styles['Heading3'],
                fontSize=16,
                spaceAfter=12,
                spaceBefore=12
            ),
            'Normal': ParagraphStyle(
                'Normal',
                parent=self.styles['Normal'],
                fontSize=12,
                leading=16,
                spaceAfter=6
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
        
        try:
            # 创建PDF文档
            doc = SimpleDocTemplate(output_path, pagesize=A4)
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
    
    def _process_blocks(self, content: Dict[str, Any], story: list):
        """
        处理文档块内容
        
        :param content: 文档内容
        :param story: PDF内容列表
        """
        blocks = content.get('items', [])
        
        for block in blocks:
            block_type = block.get('block_type')
            block_data = {
                'block_id': block.get('block_id'),
                'parent_id': block.get('parent_id'),
                'children': block.get('children', []),
                'block_type': block_type
            }
            
            # 根据块类型处理内容
            if block_type == 1:  # 页面(Page)
                self._process_page(block, story)
            elif block_type in [3, 4, 5, 6, 7, 8, 9, 10, 11]:  # 标题
                self._process_heading(block, block_type, story)
            elif block_type in [2, 12, 13, 15, 17]:  # 文本、列表、引用、待办事项
                self._process_text(block, story)
            elif block_type == 14:  # 代码块
                self._process_code(block, story)
            elif block_type == 22:  # 分割线
                self._process_divider(story)
            elif block_type == 31:  # 表格
                self._process_table(block, story)
            elif block_type == 27:  # 图片
                self._process_image(block, story)
            # 其他块类型可根据需要添加处理逻辑
    
    def _process_page(self, block: Dict[str, Any], story: list):
        """
        处理页面块
        
        :param block: 块数据
        :param story: PDF内容列表
        """
        elements = block.get('page', {}).get('elements', [])
        for element in elements:
            if 'text_run' in element:
                content = element['text_run']['content']
                story.append(Paragraph(content, self.custom_styles['Heading1']))
                story.append(Spacer(1, 12))
    
    def _process_heading(self, block: Dict[str, Any], block_type: int, story: list):
        """
        处理标题块
        
        :param block: 块数据
        :param block_type: 块类型
        :param story: PDF内容列表
        """
        elements = block.get('heading1', {}).get('elements', []) or \
                   block.get('heading2', {}).get('elements', []) or \
                   block.get('heading3', {}).get('elements', []) or \
                   block.get('heading4', {}).get('elements', []) or \
                   block.get('heading5', {}).get('elements', []) or \
                   block.get('heading6', {}).get('elements', []) or \
                   block.get('heading7', {}).get('elements', []) or \
                   block.get('heading8', {}).get('elements', []) or \
                   block.get('heading9', {}).get('elements', [])
        
        for element in elements:
            if 'text_run' in element:
                content = element['text_run']['content']
                
                # 根据标题级别选择样式
                style_name = f"Heading{block_type - 2}"  # 3->Heading1, 4->Heading2, etc.
                if style_name in self.custom_styles:
                    story.append(Paragraph(content, self.custom_styles[style_name]))
                else:
                    story.append(Paragraph(content, self.custom_styles['Heading2']))
                story.append(Spacer(1, 12))
    
    def _process_text(self, block: Dict[str, Any], story: list):
        """
        处理文本块
        
        :param block: 块数据
        :param story: PDF内容列表
        """
        # 确定使用哪个键来获取元素
        block_key = None
        if 'text' in block:
            block_key = 'text'
        elif 'bullet' in block:
            block_key = 'bullet'
        elif 'ordered' in block:
            block_key = 'ordered'
        elif 'quote' in block:
            block_key = 'quote'
        elif 'todo' in block:
            block_key = 'todo'
        
        if block_key:
            elements = block[block_key].get('elements', [])
            for element in elements:
                if 'text_run' in element:
                    content = element['text_run']['content']
                    story.append(Paragraph(content, self.custom_styles['Normal']))
                    story.append(Spacer(1, 6))
    
    def _process_code(self, block: Dict[str, Any], story: list):
        """
        处理代码块
        
        :param block: 块数据
        :param story: PDF内容列表
        """
        code_content = block.get('code', {}).get('elements', [{}])[0].get('text_run', {}).get('content', 'Empty code block')
        # 在PDF中简单地处理代码块
        story.append(Paragraph(f"<pre>{code_content}</pre>", self.custom_styles['Normal']))
        story.append(Spacer(1, 6))
    
    def _process_divider(self, story: list):
        """
        处理分割线
        
        :param story: PDF内容列表
        """
        story.append(Spacer(1, 12))
        # 在PDF中添加一条线作为分割线
        story.append(Paragraph("<br/>" + "-"*80 + "<br/>", self.custom_styles['Normal']))
        story.append(Spacer(1, 12))
    
    def _process_table(self, block: Dict[str, Any], story: list):
        """
        处理表格块
        
        :param block: 块数据
        :param story: PDF内容列表
        """
        table_data = block.get('table', {})
        cells = table_data.get('cells', [])
        property_data = table_data.get('property', {})
        row_size = property_data.get('row_size', 0)
        column_size = property_data.get('column_size', 0)
        
        if row_size > 0 and column_size > 0:
            # 创建表格数据
            table_content = []
            for i in range(row_size):
                row = []
                for j in range(column_size):
                    idx = i * column_size + j
                    if idx < len(cells):
                        row.append(cells[idx])
                    else:
                        row.append("")
                table_content.append(row)
            
            # 创建表格
            if table_content:
                pdf_table = Table(table_content)
                pdf_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 14),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(pdf_table)
                story.append(Spacer(1, 12))
    
    def _process_image(self, block: Dict[str, Any], story: list):
        """
        处理图片块
        
        :param block: 块数据
        :param story: PDF内容列表
        """
        # 图片块在PDF中需要特殊处理，因为无法直接从飞书获取图片内容
        # 这里只是添加一个占位符
        story.append(Paragraph("[图片块]", self.custom_styles['Normal']))
        story.append(Spacer(1, 6))
