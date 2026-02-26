"""
批量文档转换工具
用于从JSON文件提取文档链接并批量转换
"""

import json
import logging
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Callable
from urllib.parse import urljoin

from tqdm import tqdm

from ..converter import FeishuConverter
from ..api import FeishuDocAPI


class BatchConverter:
    """
    批量文档转换器
    支持从JSON文件提取文档链接并批量转换为指定格式
    """

    # 飞书文档URL模板
    WIKI_URL_TEMPLATE = "https://r3c0qt6yjw.feishu.cn/wiki/{token}"
    DOCX_URL_TEMPLATE = "https://r3c0qt6yjw.feishu.cn/docx/{token}"

    def __init__(
        self,
        output_dir: str,
        output_format: str = "markdown",
        max_workers: int = 3,
        delay: float = 1.0,
        progress_callback: Optional[Callable] = None,
        use_title_as_filename: bool = True
    ):
        """
        初始化批量转换器

        :param output_dir: 输出目录
        :param output_format: 输出格式 (markdown, pdf)
        :param max_workers: 最大并发数
        :param delay: 请求间隔（秒）
        :param progress_callback: 进度回调函数
        :param use_title_as_filename: 是否使用文档标题作为文件名
        """
        self.output_dir = Path(output_dir)
        self.output_format = output_format.lower()
        self.max_workers = max_workers
        self.delay = delay
        self.progress_callback = progress_callback
        self.use_title_as_filename = use_title_as_filename
        self.logger = logging.getLogger(__name__)

        # 确保输出目录存在
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 初始化转换器
        self.converter = FeishuConverter()
        self.api = FeishuDocAPI()

        # 用于跟踪已使用的文件名，避免重复
        self.used_filenames = set()

        # 统计信息
        self.stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'skipped': 0,
            'errors': []
        }

    def extract_tokens_from_json(self, json_file: str) -> List[str]:
        """
        从JSON文件中提取文档token列表

        :param json_file: JSON文件路径
        :return: 文档token列表
        """
        self.logger.info(f"正在解析JSON文件: {json_file}")

        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            tokens = []

            # 解析数据结构
            if isinstance(data, dict):
                # 检查是否是标准响应格式
                if 'data' in data and isinstance(data['data'], dict):
                    data = data['data']

                # 提取tree结构中的tokens
                if 'tree' in data and isinstance(data['tree'], dict):
                    tree = data['tree']

                    # 提取根列表
                    if 'root_list' in tree and isinstance(tree['root_list'], list):
                        tokens.extend(tree['root_list'])
                        self.logger.info(f"从root_list提取到 {len(tree['root_list'])} 个token")

                    # 提取child_map中的所有子节点
                    if 'child_map' in tree and isinstance(tree['child_map'], dict):
                        for parent_token, child_tokens in tree['child_map'].items():
                            if isinstance(child_tokens, list):
                                tokens.extend(child_tokens)
                        self.logger.info(f"从child_map提取到子节点")

                # 直接提取其他可能的token列表
                for key in ['tokens', 'items', 'documents', 'nodes']:
                    if key in data and isinstance(data[key], list):
                        tokens.extend(data[key])

            elif isinstance(data, list):
                # 如果是列表，直接使用
                tokens = data

            # 去重并保持顺序
            seen = set()
            unique_tokens = []
            for token in tokens:
                if isinstance(token, str) and token not in seen:
                    # 验证token格式（飞书token通常是22字符的字母数字组合）
                    if re.match(r'^[a-zA-Z0-9_-]{20,30}$', token):
                        seen.add(token)
                        unique_tokens.append(token)

            self.logger.info(f"共提取到 {len(unique_tokens)} 个唯一文档token")
            return unique_tokens

        except json.JSONDecodeError as e:
            self.logger.error(f"JSON解析失败: {e}")
            raise
        except Exception as e:
            self.logger.error(f"读取文件失败: {e}")
            raise

    def token_to_url(self, token: str, doc_type: str = "wiki") -> str:
        """
        将token转换为完整的飞书文档URL

        :param token: 文档token
        :param doc_type: 文档类型 (wiki, docx)
        :return: 完整的URL
        """
        if doc_type == "wiki":
            return self.WIKI_URL_TEMPLATE.format(token=token)
        else:
            return self.DOCX_URL_TEMPLATE.format(token=token)

    def get_document_title(self, token: str, doc_type: str = "wiki") -> Optional[str]:
        """
        获取文档标题

        :param token: 文档token
        :param doc_type: 文档类型
        :return: 文档标题，失败返回None
        """
        try:
            # 获取文档信息
            doc_info = self.api.get_document_info(token)
            if doc_info:
                # 尝试获取标题
                title = doc_info.get('title')
                if title:
                    return title
        except Exception as e:
            self.logger.warning(f"获取文档标题失败 {token}: {e}")

        return None

    def generate_filename(self, token: str, title: Optional[str] = None) -> str:
        """
        生成安全的文件名

        :param token: 文档token
        :param title: 文档标题
        :return: 安全的文件名
        """
        if title and self.use_title_as_filename:
            # 使用标题作为基础文件名
            base_name = self._sanitize_filename(title)
            # 如果标题为空或清理后为空，使用token
            if not base_name:
                base_name = token[:20]
        else:
            # 使用token作为文件名
            base_name = token

        # 确保文件名唯一
        filename = base_name
        counter = 1
        while filename in self.used_filenames:
            filename = f"{base_name}_{counter}"
            counter += 1

        self.used_filenames.add(filename)
        return filename

    def convert_single(
        self,
        token: str,
        index: int,
        total: int,
        doc_type: str = "wiki"
    ) -> Tuple[str, bool, Optional[str]]:
        """
        转换单个文档

        :param token: 文档token
        :param index: 当前索引
        :param total: 总数
        :param doc_type: 文档类型
        :return: (token, 是否成功, 输出文件路径或错误信息)
        """
        url = self.token_to_url(token, doc_type)

        # 获取文档标题
        title = None
        if self.use_title_as_filename:
            title = self.get_document_title(token, doc_type)

        # 生成文件名
        filename = self.generate_filename(token, title)
        output_path = self.output_dir / f"{filename}.{self.output_format}"

        # 检查是否已存在
        if output_path.exists():
            self.logger.info(f"[{index}/{total}] 已存在，跳过: {filename}")
            return token, True, str(output_path)

        display_name = title if title else token[:20]
        self.logger.info(f"[{index}/{total}] 正在转换: {display_name}")

        try:
            # 添加延迟避免请求过快
            if self.delay > 0:
                time.sleep(self.delay)

            # 执行转换
            success = self.converter.convert(
                document_url=url,
                output_format=self.output_format,
                output_path=str(output_path)
            )

            if success and output_path.exists():
                self.logger.info(f"[{index}/{total}] 转换成功: {filename}")
                return token, True, str(output_path)
            else:
                error_msg = "转换失败或输出文件未生成"
                self.logger.error(f"[{index}/{total}] 转换失败: {filename} - {error_msg}")
                return token, False, error_msg

        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"[{index}/{total}] 转换异常: {filename} - {error_msg}")
            return token, False, error_msg

    def convert_all(
        self,
        tokens: List[str],
        doc_type: str = "wiki",
        use_parallel: bool = False
    ) -> Dict:
        """
        批量转换所有文档

        :param tokens: 文档token列表
        :param doc_type: 文档类型
        :param use_parallel: 是否使用并行处理
        :return: 转换结果统计
        """
        self.stats = {
            'total': len(tokens),
            'success': 0,
            'failed': 0,
            'skipped': 0,
            'errors': [],
            'results': []
        }

        # 重置已使用文件名集合
        self.used_filenames = set()

        total = len(tokens)
        self.logger.info(f"开始批量转换 {total} 个文档")

        if use_parallel and self.max_workers > 1:
            # 并行处理
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {
                    executor.submit(
                        self.convert_single,
                        token,
                        i + 1,
                        total,
                        doc_type
                    ): token
                    for i, token in enumerate(tokens)
                }

                # 使用tqdm显示进度
                with tqdm(total=total, desc="转换进度") as pbar:
                    for future in as_completed(futures):
                        token, success, result = future.result()
                        self._update_stats(token, success, result)
                        pbar.update(1)

                        # 调用进度回调
                        if self.progress_callback:
                            self.progress_callback(token, success, result)
        else:
            # 串行处理
            for i, token in enumerate(tqdm(tokens, desc="转换进度")):
                token, success, result = self.convert_single(
                    token, i + 1, total, doc_type
                )
                self._update_stats(token, success, result)

                # 调用进度回调
                if self.progress_callback:
                    self.progress_callback(token, success, result)

        # 生成报告
        self._generate_report()

        return self.stats

    def _update_stats(self, token: str, success: bool, result: str):
        """更新统计信息"""
        if success:
            if "跳过" in result or (isinstance(result, str) and Path(result).exists()):
                # 检查是否是已存在的文件
                if Path(result).exists() and self.stats['results']:
                    # 检查是否之前已经处理过
                    existing = [r for r in self.stats['results'] if r['token'] == token and r['success']]
                    if existing:
                        self.stats['skipped'] += 1
                    else:
                        self.stats['success'] += 1
                else:
                    self.stats['success'] += 1
            else:
                self.stats['success'] += 1
        else:
            self.stats['failed'] += 1
            self.stats['errors'].append({
                'token': token,
                'error': result
            })

        self.stats['results'].append({
            'token': token,
            'success': success,
            'result': result
        })

    def _generate_report(self):
        """生成转换报告"""
        report_path = self.output_dir / "conversion_report.json"

        report = {
            'summary': {
                'total': self.stats['total'],
                'success': self.stats['success'],
                'failed': self.stats['failed'],
                'skipped': self.stats['skipped'],
                'success_rate': f"{(self.stats['success'] / self.stats['total'] * 100):.2f}%"
            },
            'errors': self.stats['errors'],
            'results': self.stats['results']
        }

        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        self.logger.info(f"转换报告已保存: {report_path}")
        self.logger.info(f"转换完成: 总计 {self.stats['total']}, "
                        f"成功 {self.stats['success']}, "
                        f"失败 {self.stats['failed']}, "
                        f"跳过 {self.stats['skipped']}")

    def _sanitize_filename(self, title: str) -> str:
        """
        生成安全的文件名

        :param title: 文档标题
        :return: 安全的文件名
        """
        if not title:
            return ""

        # 移除或替换不安全的字符
        # 保留中文、英文、数字、空格、连字符和下划线
        safe_name = re.sub(r'[<>:"/\\|?*]', '', title)
        # 将多个空格替换为单个空格
        safe_name = re.sub(r'\s+', ' ', safe_name)
        # 去除首尾空格
        safe_name = safe_name.strip()
        # 如果文件名太长，截断
        if len(safe_name) > 100:
            safe_name = safe_name[:100]

        return safe_name


def convert_from_json_file(
    json_file: str,
    output_dir: str,
    output_format: str = "markdown",
    doc_type: str = "wiki",
    max_workers: int = 1,
    delay: float = 1.0,
    progress_callback: Optional[Callable] = None,
    use_title_as_filename: bool = True
) -> Dict:
    """
    从JSON文件批量转换文档的便捷函数

    :param json_file: JSON文件路径
    :param output_dir: 输出目录
    :param output_format: 输出格式 (markdown, pdf)
    :param doc_type: 文档类型 (wiki, docx)
    :param max_workers: 最大并发数
    :param delay: 请求间隔（秒）
    :param progress_callback: 进度回调函数
    :param use_title_as_filename: 是否使用文档标题作为文件名
    :return: 转换结果统计
    """
    # 创建转换器
    converter = BatchConverter(
        output_dir=output_dir,
        output_format=output_format,
        max_workers=max_workers,
        delay=delay,
        progress_callback=progress_callback,
        use_title_as_filename=use_title_as_filename
    )

    # 提取tokens
    tokens = converter.extract_tokens_from_json(json_file)

    if not tokens:
        logging.warning("未找到任何文档token")
        return {
            'total': 0,
            'success': 0,
            'failed': 0,
            'skipped': 0,
            'errors': [],
            'results': []
        }

    # 执行批量转换
    return converter.convert_all(tokens, doc_type, use_parallel=max_workers > 1)


# 命令行入口
def main():
    """命令行入口"""
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description='批量转换飞书文档',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s get_info.json ./output markdown
  %(prog)s get_info.json ./output pdf --doc-type wiki --workers 3
  %(prog)s get_info.json ./output markdown --delay 0.5
  %(prog)s get_info.json ./output markdown --use-token-filename  # 使用token作为文件名
        """
    )

    parser.add_argument('json_file', help='包含文档token的JSON文件路径')
    parser.add_argument('output_dir', help='输出目录')
    parser.add_argument(
        'format',
        choices=['markdown', 'md', 'pdf'],
        default='markdown',
        help='输出格式'
    )

    parser.add_argument(
        '--doc-type',
        choices=['wiki', 'docx'],
        default='wiki',
        help='文档类型 (默认: wiki)'
    )

    parser.add_argument(
        '--workers',
        type=int,
        default=1,
        help='并发数 (默认: 1)'
    )

    parser.add_argument(
        '--delay',
        type=float,
        default=1.0,
        help='请求间隔秒数 (默认: 1.0)'
    )

    parser.add_argument(
        '--use-token-filename',
        action='store_true',
        help='使用token作为文件名（默认使用文档标题）'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='显示详细日志'
    )

    args = parser.parse_args()

    # 设置日志
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # 检查文件是否存在
    if not os.path.exists(args.json_file):
        print(f"错误: 文件不存在: {args.json_file}", file=sys.stderr)
        sys.exit(1)

    # 标准化格式
    output_format = 'markdown' if args.format in ['markdown', 'md'] else 'pdf'

    # 执行转换
    try:
        stats = convert_from_json_file(
            json_file=args.json_file,
            output_dir=args.output_dir,
            output_format=output_format,
            doc_type=args.doc_type,
            max_workers=args.workers,
            delay=args.delay,
            use_title_as_filename=not args.use_token_filename
        )

        # 输出结果
        print("\n" + "=" * 50)
        print("批量转换完成!")
        print("=" * 50)
        print(f"总计: {stats['total']}")
        print(f"成功: {stats['success']}")
        print(f"失败: {stats['failed']}")
        print(f"跳过: {stats.get('skipped', 0)}")

        if stats['errors']:
            print(f"\n错误详情 ({len(stats['errors'])} 个):")
            for error in stats['errors'][:5]:  # 只显示前5个错误
                print(f"  - {error['token']}: {error['error']}")
            if len(stats['errors']) > 5:
                print(f"  ... 还有 {len(stats['errors']) - 5} 个错误")

        # 根据结果设置退出码
        sys.exit(0 if stats['failed'] == 0 else 1)

    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
