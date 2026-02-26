"""
PDF转Markdown工具
将PDF文件转换为Markdown格式
"""

import os
import re
from typing import Optional, List, Dict, Tuple
from collections import Counter
import pdfplumber


class PdfToMarkdownConverter:
    """
    PDF转Markdown转换器
    基于PDF的字体大小和样式信息来识别标题和内容
    """
    
    def __init__(self):
        """
        初始化PDF转Markdown转换器
        """
        pass
    
    def convert(self, pdf_path: str, output_path: Optional[str] = None) -> str:
        """
        将PDF文件转换为Markdown格式
        
        :param pdf_path: PDF文件路径
        :param output_path: 输出Markdown文件路径，若为None则不保存文件
        :return: 转换后的Markdown内容
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
        
        markdown_content = self._read_pdf(pdf_path)
        
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
        
        return markdown_content
    
    def _read_pdf(self, pdf_path: str) -> str:
        """
        读取PDF文件内容并转换为Markdown格式
        
        :param pdf_path: PDF文件路径
        :return: 转换后的Markdown内容
        """
        markdown_lines = []
        
        with pdfplumber.open(pdf_path) as pdf:
            all_font_sizes = []
            
            for page in pdf.pages:
                chars = page.chars
                for char in chars:
                    if 'size' in char:
                        all_font_sizes.append(round(char['size'], 1))
            
            font_size_counter = Counter(all_font_sizes)
            most_common_sizes = font_size_counter.most_common(10)
            
            body_size = self._find_body_size(most_common_sizes)
            heading_sizes = self._find_heading_sizes(most_common_sizes, body_size)
            
            for page_num, page in enumerate(pdf.pages, 1):
                page_content = self._process_page_with_fonts(page, page_num, heading_sizes, body_size)
                markdown_lines.extend(page_content)
                markdown_lines.append('')
        
        return '\n'.join(markdown_lines)
    
    def _find_body_size(self, most_common_sizes: List[Tuple[float, int]]) -> float:
        """
        找出正文字体大小（出现次数最多的）
        
        :param most_common_sizes: 最常见的字体大小列表
        :return: 正文字体大小
        """
        if most_common_sizes:
            return most_common_sizes[0][0]
        return 12.0
    
    def _find_heading_sizes(self, most_common_sizes: List[Tuple[float, int]], body_size: float) -> Dict[int, float]:
        """
        找出各级标题的字体大小
        
        :param most_common_sizes: 最常见的字体大小列表
        :param body_size: 正文字体大小
        :return: 各级标题的字体大小字典
        """
        sizes = sorted([size for size, count in most_common_sizes if size > body_size], reverse=True)
        
        heading_sizes = {}
        
        for i, size in enumerate(sizes):
            heading_sizes[i + 1] = size
        
        return heading_sizes
    
    def _process_page_with_fonts(self, page, page_num: int, heading_sizes: Dict[int, float], body_size: float) -> List[str]:
        """
        使用字体信息处理页面内容
        
        :param page: pdfplumber页面对象
        :param page_num: 页码
        :param heading_sizes: 各级标题的字体大小
        :param body_size: 正文字体大小
        :return: Markdown格式的内容行列表
        """
        markdown_lines = []
        
        words = page.extract_words(extra_attrs=['fontname', 'size'], keep_blank_chars=False)
        
        if not words:
            return markdown_lines
        
        lines = self._group_words_into_lines(words)
        
        for i, line_data in enumerate(lines):
            text = line_data['text'].strip()
            avg_size = line_data['avg_size']
            
            if not text:
                markdown_lines.append('')
                continue
            
            text = self._clean_text(text)
            if not text:
                continue
            
            if page_num == 1 and i == 0:
                markdown_lines.append(f"# {text}")
                markdown_lines.append('')
                continue
            
            heading_level = self._determine_heading_level_by_size(avg_size, heading_sizes, body_size)
            
            if heading_level:
                if markdown_lines and markdown_lines[-1]:
                    markdown_lines.append('')
                heading_prefix = '#' * heading_level
                markdown_lines.append(f"{heading_prefix} {text}")
                markdown_lines.append('')
            elif self._is_sub_list_item(text):
                markdown_lines.append(f"   {text}")
            elif self._is_quote(text):
                markdown_lines.append(f"> {text}")
            else:
                markdown_lines.append(text)
        
        return markdown_lines
    
    def _group_words_into_lines(self, words: List[Dict]) -> List[Dict]:
        """
        将单词按行分组
        
        :param words: 单词列表
        :return: 行数据列表
        """
        if not words:
            return []
        
        words_sorted = sorted(words, key=lambda w: (round(w.get('top', 0), 0), w.get('x0', 0)))
        
        lines = []
        current_line = []
        current_top = None
        tolerance = 3
        
        for word in words_sorted:
            word_top = round(word.get('top', 0), 0)
            
            if current_top is None:
                current_top = word_top
                current_line = [word]
            elif abs(word_top - current_top) <= tolerance:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(self._create_line_data(current_line))
                current_line = [word]
                current_top = word_top
        
        if current_line:
            lines.append(self._create_line_data(current_line))
        
        return lines
    
    def _create_line_data(self, words: List[Dict]) -> Dict:
        """
        从单词列表创建行数据
        
        :param words: 单词列表
        :return: 行数据字典
        """
        words_sorted = sorted(words, key=lambda w: w.get('x0', 0))
        text = ' '.join(w.get('text', '') for w in words_sorted)
        
        sizes = [w.get('size', 12) for w in words_sorted if w.get('size')]
        avg_size = sum(sizes) / len(sizes) if sizes else 12.0
        
        return {
            'text': text,
            'avg_size': avg_size,
            'words': words_sorted
        }
    
    def _determine_heading_level_by_size(self, size: float, heading_sizes: Dict[int, float], body_size: float) -> Optional[int]:
        """
        根据字体大小确定标题级别
        
        :param size: 字体大小
        :param heading_sizes: 各级标题的字体大小
        :param body_size: 正文字体大小
        :return: 标题级别（1-5），如果不是标题则返回None
        """
        if size <= body_size:
            return None
        
        for level in sorted(heading_sizes.keys()):
            if size >= heading_sizes[level]:
                return level
        
        return None
    
    def _clean_text(self, text: str) -> str:
        """
        清理文本中的异常字符
        
        :param text: 原始文本
        :return: 清理后的文本
        """
        clean_text = ''.join(c for c in text if ord(c) >= 32 or c in '\n\t')
        clean_text = ' '.join(clean_text.split())
        return clean_text
    
    def _is_list_item(self, line: str) -> bool:
        """
        判断是否为列表项
        
        :param line: 文本行
        :return: 是否为列表项
        """
        return bool(re.match(r'^(\d+\.|[-*•])\s', line))
    
    def _is_sub_list_item(self, line: str) -> bool:
        """
        判断是否为子列表项
        
        :param line: 文本行
        :return: 是否为子列表项
        """
        return bool(re.match(r'^([a-z]\.|[ivx]+\.)\s', line, re.IGNORECASE))
    
    def _is_quote(self, line: str) -> bool:
        """
        判断是否为引用
        
        :param line: 文本行
        :return: 是否为引用
        """
        return line.startswith('"') or line.startswith('"') or line.startswith('"')


def convert_pdf_to_markdown(pdf_path: str, output_path: Optional[str] = None) -> str:
    """
    将PDF文件转换为Markdown格式的便捷函数
    
    :param pdf_path: PDF文件路径
    :param output_path: 输出Markdown文件路径，若为None则不保存文件
    :return: 转换后的Markdown内容
    """
    converter = PdfToMarkdownConverter()
    return converter.convert(pdf_path, output_path)
