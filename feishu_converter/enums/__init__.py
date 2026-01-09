from enum import Enum


class Align(Enum):
    """块的排版方式"""
    LEFT = 1  # 居左排版
    CENTER = 2  # 居中排版
    RIGHT = 3  # 居右排版


class BlockType(Enum):
    """块类型枚举"""
    PAGE = 1  # 页面 Block
    TEXT = 2  # 文本 Block
    HEADING1 = 3  # 标题 1 Block
    HEADING2 = 4  # 标题 2 Block
    HEADING3 = 5  # 标题 3 Block
    HEADING4 = 6  # 标题 4 Block
    HEADING5 = 7  # 标题 5 Block
    HEADING6 = 8  # 标题 6 Block
    HEADING7 = 9  # 标题 7 Block
    HEADING8 = 10  # 标题 8 Block
    HEADING9 = 11  # 标题 9 Block
    BULLET = 12  # 无序列表 Block
    ORDERED = 13  # 有序列表 Block
    CODE = 14  # 代码块 Block
    QUOTE = 15  # 引用 Block
    # 16 缺失
    TODO = 17  # 待办事项 Block
    BITABLE = 18  # 多维表格 Block
    CALLOUT = 19  # 高亮块 Block
    CHAT_CARD = 20  # 会话卡片 Block
    DIAGRAM = 21  # 流程图 & UML Block
    DIVIDER = 22  # 分割线 Block
    FILE = 23  # 文件 Block
    GRID = 24  # 分栏 Block
    GRID_COLUMN = 25  # 分栏列 Block
    IFRAME = 26  # 内嵌 Block Block
    IMAGE = 27  # 图片 Block
    ISV = 28  # 开放平台小组件 Block
    MINDNOTE = 29  # 思维笔记 Block
    SHEET = 30  # 电子表格 Block
    TABLE = 31  # 表格 Block
    TABLE_CELL = 32  # 表格单元格 Block
    VIEW = 33  # 视图 Block
    QUOTE_CONTAINER = 34  # 引用容器 Block
    TASK = 35  # 任务 Block
    OKR = 36  # OKR Block
    OKR_OBJECTIVE = 37  # OKR Objective Block
    OKR_KEY_RESULT = 38  # OKR Key Result Block
    OKR_PROGRESS = 39  # OKR Progress Block
    ADD_ONS = 40  # 新版文档小组件 Block
    JIRA_ISSUE = 41  # Jira 问题 Block
    WIKI_CATALOG = 42  # Wiki 子页面列表 Block（旧版）
    BOARD = 43  # 画板 Block
    AGENDA = 44  # 议程 Block
    AGENDA_ITEM = 45  # 议程项 Block
    AGENDA_ITEM_TITLE = 46  # 议程项标题 Block
    AGENDA_ITEM_CONTENT = 47  # 议程项内容 Block
    LINK_PREVIEW = 48  # 链接预览 Block
    SOURCE_SYNCED = 49  # 源同步块
    REFERENCE_SYNCED = 50  # 引用同步块
    SUB_PAGE_LIST = 51  # Wiki 子页面列表 Block（新版）
    AI_TEMPLATE = 52  # AI 模板 Block
    UNDEFINED = 999  # 未支持 Block


class BitableViewType(Enum):
    """Bitable Block 的视图类型"""
    GRID = 1  # 数据表
    KANBAN = 2  # 看板


class CalloutBackgroundColor(Enum):
    """高亮块的背景色"""
    LIGHT_RED = 1  # 浅红色
    LIGHT_ORANGE = 2  # 浅橙色
    LIGHT_YELLOW = 3  # 浅黄色
    LIGHT_GREEN = 4  # 浅绿色
    LIGHT_BLUE = 5  # 浅蓝色
    LIGHT_PURPLE = 6  # 浅紫色
    LIGHT_GRAY = 7  # 中灰色
    MEDIUM_RED = 8  # 中红色
    MEDIUM_ORANGE = 9  # 中橙色
    MEDIUM_YELLOW = 10  # 中黄色
    MEDIUM_GREEN = 11  # 中绿色
    MEDIUM_BLUE = 12  # 中蓝色
    MEDIUM_PURPLE = 13  # 中紫色
    GRAY = 14  # 灰色
    PALE_GRAY = 15  # 浅灰色


class CalloutBorderColor(Enum):
    """高亮块的边框色"""
    RED = 1  # 红色
    ORANGE = 2  # 橙色
    YELLOW = 3  # 黄色
    GREEN = 4  # 绿色
    BLUE = 5  # 蓝色
    PURPLE = 6  # 紫色
    GRAY = 7  # 灰色


class CodeLanguage(Enum):
    """代码块语言"""
    PLAIN_TEXT = 1  # PlainText
    ABAP = 2
    ADA = 3
    APACHE = 4
    APEX = 5
    ASSEMBLY = 6
    BASH = 7
    CSHARP = 8  # CSharp
    CPP = 9  # C++
    C = 10
    COBOL = 11
    CSS = 12
    COFFEESCRIPT = 13  # CoffeeScript
    D = 14
    DART = 15
    DELPHI = 16
    DJANGO = 17
    DOCKERFILE = 18
    ERLANG = 19
    FORTRAN = 20
    FOXPRO = 21  # FoxPro
    GO = 22
    GROOVY = 23
    HTML = 24
    HTMLBARS = 25  # HTMLBars
    HTTP = 26
    HASKELL = 27
    JSON = 28
    JAVA = 29
    JAVASCRIPT = 30
    JULIA = 31
    KOTLIN = 32
    LATEX = 33  # LateX
    LISP = 34
    LOGO = 35
    LUA = 36
    MATLAB = 37
    MAKEFILE = 38
    MARKDOWN = 39
    NGINX = 40
    OBJECTIVE = 41  # Objective
    OPENEDGEABL = 42  # OpenEdgeABL
    PHP = 43
    PERL = 44
    POSTSCRIPT = 45
    POWERSHELL = 46
    PROLOG = 47
    PROTOBUF = 48  # ProtoBuf
    PYTHON = 49
    R = 50
    RPG = 51
    RUBY = 52
    RUST = 53
    SAS = 54
    SCSS = 55
    SQL = 56
    SCALA = 57
    SCHEME = 58
    SCRATCH = 59
    SHELL = 60
    SWIFT = 61
    THRIFT = 62
    TYPESCRIPT = 63
    VBSCRIPT = 64
    VISUAL = 65  # Visual
    XML = 66
    YAML = 67
    CMAKE = 68
    DIFF = 69
    GHERKIN = 70
    GRAPHQL = 71
    OPENGL_SHADING_LANGUAGE = 72  # OpenGL Shading Language
    PROPERTIES = 73
    SOLIDITY = 74
    TOML = 75


class DiagramType(Enum):
    """绘图类型"""
    FLOW_CHART = 1  # 流程图
    UML = 2  # UML 图


class FontBackgroundColor(Enum):
    """字体的背景色"""
    LIGHT_RED = 1  # 浅红色
    LIGHT_ORANGE = 2  # 浅橙色
    LIGHT_YELLOW = 3  # 浅黄色
    LIGHT_GREEN = 4  # 浅绿色
    LIGHT_BLUE = 5  # 浅蓝色
    LIGHT_PURPLE = 6  # 浅紫色
    LIGHT_GRAY = 7  # 中灰色
    RED = 8  # 红色
    ORANGE = 9  # 橙色
    YELLOW = 10  # 黄色
    GREEN = 11  # 绿色
    BLUE = 12  # 蓝色
    PURPLE = 13  # 紫色
    GRAY = 14  # 灰色
    PALE_GRAY = 15  # 浅灰色


class FontColor(Enum):
    """字体色"""
    RED = 1  # 红色
    ORANGE = 2  # 橙色
    YELLOW = 3  # 黄色
    GREEN = 4  # 绿色
    BLUE = 5  # 蓝色
    PURPLE = 6  # 紫色
    GRAY = 7  # 灰色


class IframeComponentType(Enum):
    """内嵌 Block 支持的类型"""
    BILIBILI = 1  # 哔哩哔哩
    XIGUA = 2  # 西瓜视频
    YOUKU = 3  # 优酷
    AIRTABLE = 4  # Airtable
    BAIDU_MAP = 5  # 百度地图
    GAODE_MAP = 6  # 高德地图
    UNDEFINED_7 = 7  # Undefined
    FIGMA = 8  # Figma
    MODAO = 9  # 墨刀
    CANVA = 10  # Canva
    CODEPEN = 11  # CodePen
    FEISHU_FORM = 12  # 飞书问卷
    JINSHUJU = 13  # 金数据
    UNDEFINED_14 = 14  # Undefined
    UNDEFINED_15 = 15  # Undefined


class LinkPreviewURLType(Enum):
    """链接预览 Block 支持的链接类型"""
    MESSAGE_LINK = "MessageLink"  # IM 消息链接
    UNDEFINED = "Undefined"  # 未定义的链接类型


class MentionObjType(Enum):
    """Mention 云文档类型"""
    DOC = 1  # Doc
    SHEET = 3  # Sheet
    BITABLE = 8  # Bitable
    MINDNOTE = 11  # MindNote
    FILE = 12  # File
    SLIDE = 15  # Slide
    WIKI = 16  # Wiki
    DOCX = 22  # Docx


class OkrPeriodDisplayStatus(Enum):
    """OKR 周期的状态"""
    DEFAULT = "default"  # 默认
    NORMAL = "normal"  # 正常
    INVALID = "invalid"  # 失效
    HIDDEN = "hidden"  # 隐藏


class OkrProgressRateMode(Enum):
    """OKR 进展状态模式"""
    SIMPLE = "simple"  # 简单模式
    ADVANCED = "advanced"  # 高级模式


class OkrProgressStatus(Enum):
    """OKR 进展状态"""
    UNSET = "unset"  # 未设置
    NORMAL = "normal"  # 正常
    RISK = "risk"  # 有风险
    EXTENDED = "extended"  # 已延期


class OkrProgressStatusType(Enum):
    """OKR 进展所展示的状态计算类型"""
    DEFAULT = "default"  # 以风险最高的 Key Result 状态展示
    CUSTOM = "custom"  # 自定义


class TextBackgroundColor(Enum):
    """文本块的块级别背景色"""
    LIGHT_GRAY = "LightGrayBackground"  # 浅灰色
    LIGHT_RED = "LightRedBackground"  # 浅红色
    LIGHT_ORANGE = "LightOrangeBackground"  # 浅橙色
    LIGHT_YELLOW = "LightYellowBackground"  # 浅黄色
    LIGHT_GREEN = "LightGreenBackground"  # 浅绿色
    LIGHT_BLUE = "LightBlueBackground"  # 浅蓝色
    LIGHT_PURPLE = "LightPurpleBackground"  # 浅紫色
    PALE_GRAY = "PaleGrayBackground"  # 中灰色
    DARK_GRAY = "DarkGrayBackground"  # 灰色
    DARK_RED = "DarkRedBackground"  # 中红色
    DARK_ORANGE = "DarkOrangeBackground"  # 中橙色
    DARK_YELLOW = "DarkYellowBackground"  # 中黄色
    DARK_GREEN = "DarkGreenBackground"  # 中绿色
    DARK_BLUE = "DarkBlueBackground"  # 中蓝色
    DARK_PURPLE = "DarkPurpleBackground"  # 中紫色


class TextElementType(Enum):
    """文本元素类型"""
    TEXT_RUN = "text_run"  # 文字
    MENTION_USER = "mention_user"  # @用户
    MENTION_DOC = "mention_doc"  # @文档
    FILE = "file"  # @文件
    REMINDER = "reminder"  # 日期提醒
    UNDEFINED = "undefined"  # 未支持元素
    EQUATION = "equation"  # 公式


class TextIndentationLevel(Enum):
    """文本块首行缩进级别"""
    NO_INDENT = "NoIndent"  # 无缩进
    ONE_LEVEL_INDENT = "OneLevelIndent"  # 一级缩进


class ViewType(Enum):
    """View Block 的视图类型"""
    CARD = 1  # 卡片视图，独占一行的一种视图，在 Card 上可有一些简单交互
    PREVIEW = 2  # 预览视图，在当前页面直接预览插入的 Block 内容，而不需要打开新的页面
    INLINE = 3  # 内联视图