#!/bin/bash
clear
set -e  # 遇到错误时终止脚本

# 飞书文档转换脚本
# 功能：创建虚拟环境、安装依赖、执行文档转换（单文档或批量）
# 用法: 
#   ./start.sh convert <飞书文档URL> [格式]     # 单文档转换
#   ./start.sh batch <json文件> <输出目录> [格式]  # 批量转换
#
# 格式可选: markdown (默认), pdf

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的信息
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_highlight() {
    echo -e "${BLUE}[BATCH]${NC} $1"
}

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 检查Python版本
check_python_version() {
    if ! command_exists python3; then
        print_error "Python 3 is not installed or not in PATH"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    MIN_VERSION="3.6"
    
    if [[ "$(printf '%s\n' "$MIN_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$MIN_VERSION" ]]; then
        print_error "Python version must be at least $MIN_VERSION, current version is $PYTHON_VERSION"
        exit 1
    fi
    
    print_info "Python version: $PYTHON_VERSION"
}

# 检查是否在项目根目录
check_project_dir() {
    if [[ ! -f "requirements.txt" || ! -f "main.py" || ! -d "feishu_converter" ]]; then
        print_error "This script must be run from the project root directory"
        exit 1
    fi
}

# 创建虚拟环境
create_venv() {
    VENV_NAME="venv"
    
    if [[ -d "$VENV_NAME" ]]; then
        print_info "Virtual environment already exists: $VENV_NAME"
        return 0
    fi
    
    print_info "Creating virtual environment: $VENV_NAME"
    
    python3 -m venv "$VENV_NAME"
    
    if [[ $? -ne 0 ]]; then
        print_error "Failed to create virtual environment"
        exit 1
    fi
    
    print_info "Virtual environment created successfully"
}

# 激活虚拟环境
activate_venv() {
    VENV_NAME="venv"
    
    if [[ ! -d "$VENV_NAME" ]]; then
        print_error "Virtual environment does not exist: $VENV_NAME"
        exit 1
    fi
    
    print_info "Activating virtual environment: $VENV_NAME"
    
    source "$VENV_NAME/bin/activate"
    
    if [[ $? -ne 0 ]]; then
        print_error "Failed to activate virtual environment"
        exit 1
    fi
}

# 安装依赖
install_dependencies() {
    if [[ ! -f "requirements.txt" ]]; then
        print_error "requirements.txt not found"
        exit 1
    fi
    
    print_info "Installing dependencies from requirements.txt"
    
    pip install --upgrade pip
    pip install -r requirements.txt
    
    if [[ $? -ne 0 ]]; then
        print_error "Failed to install dependencies"
        exit 1
    fi
    
    print_info "Dependencies installed successfully"
}

# 检查环境变量
check_env_vars() {
    if [[ ! -f ".env" ]]; then
        print_warning ".env file not found, creating from .env.example"
        if [[ -f ".env.example" ]]; then
            cp .env.example .env
            print_info ".env file created, please edit it to add your credentials"
            exit 1
        else
            print_error ".env.example file not found"
            exit 1
        fi
    fi
    
    # 加载环境变量
    export $(grep -v '^#' .env | xargs)
    
    if [[ -z "$FEISHU_APP_ID" || -z "$FEISHU_APP_SECRET" ]]; then
        print_error "FEISHU_APP_ID or FEISHU_APP_SECRET not set in .env file"
        exit 1
    fi
    
    print_info "Environment variables loaded successfully"
}

# 执行单文档转换
execute_conversion() {
    DOCUMENT_URL="$1"
    OUTPUT_FORMAT="${2:-markdown}"  # 默认为md格式
    
    if [[ -z "$DOCUMENT_URL" ]]; then
        print_error "Usage: $0 convert <feishu_doc_url> [output_format]"
        print_info "Supported formats: pdf, markdown"
        exit 1
    fi
    
    print_info "Converting document: $DOCUMENT_URL"
    print_info "Output format: $OUTPUT_FORMAT"
    
    # 生成输出文件名
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    if [ "$OUTPUT_FORMAT" = "pdf" ]; then
        OUTPUT_FILE="./output/document_${TIMESTAMP}.pdf"
    else
        OUTPUT_FILE="./output/document_${TIMESTAMP}.md"
    fi
    
    # 确保输出目录存在
    mkdir -p ./output
    
    # 执行转换命令
    python main.py "$DOCUMENT_URL" "$OUTPUT_FORMAT" "$OUTPUT_FILE"
    
    # 检查命令执行结果
    if [ $? -eq 0 ]; then
        print_info "文档转换完成: $OUTPUT_FILE"
    else
        print_error "文档转换失败"
        exit 1
    fi
}

# 执行批量转换
execute_batch_conversion() {
    JSON_FILE="$1"
    OUTPUT_DIR="${2:-./batch_output}"
    OUTPUT_FORMAT="${3:-markdown}"  # 默认为md格式
    
    # 参数检查
    if [[ -z "$JSON_FILE" ]]; then
        print_error "Usage: $0 batch <json_file> [output_dir] [format]"
        print_info "Example: $0 batch get_info.json ./output markdown"
        exit 1
    fi
    
    # 检查JSON文件是否存在
    if [[ ! -f "$JSON_FILE" ]]; then
        print_error "JSON file not found: $JSON_FILE"
        exit 1
    fi
    
    print_highlight "========================================"
    print_highlight "      批量文档转换模式"
    print_highlight "========================================"
    print_info "JSON文件: $JSON_FILE"
    print_info "输出目录: $OUTPUT_DIR"
    print_info "输出格式: $OUTPUT_FORMAT"
    print_info "请求间隔: 6秒（避免触发API限制）"
    print_highlight "========================================"
    
    # 确保输出目录存在
    mkdir -p "$OUTPUT_DIR"
    
    # 执行批量转换
    # 使用 --delay 6 参数设置6秒间隔
    # 使用 --workers 1 参数确保串行处理（配合delay更安全）
    # 默认使用文档标题作为文件名
    python batch_convert.py "$JSON_FILE" "$OUTPUT_DIR" "$OUTPUT_FORMAT" --delay 6.0 --workers 1
    
    # 检查命令执行结果
    if [ $? -eq 0 ]; then
        print_highlight "========================================"
        print_highlight "      批量转换完成！"
        print_highlight "========================================"
        print_info "输出目录: $OUTPUT_DIR"
        
        # 显示转换报告
        if [[ -f "$OUTPUT_DIR/conversion_report.json" ]]; then
            print_info "转换报告: $OUTPUT_DIR/conversion_report.json"
            
            # 尝试解析并显示摘要（如果安装了jq）
            if command_exists jq; then
                echo ""
                print_highlight "转换统计:"
                jq -r '.summary | to_entries[] | "  \(.key): \(.value)"' "$OUTPUT_DIR/conversion_report.json"
            fi
        fi
    else
        print_error "批量转换过程中出现错误"
        exit 1
    fi
}

# 显示帮助信息
show_help() {
    echo ""
    echo "========================================"
    echo "    飞书文档转换器"
    echo "========================================"
    echo ""
    echo "用法: $0 <命令> [参数]"
    echo ""
    echo "命令:"
    echo ""
    echo "  1. 单文档转换:"
    echo "     $0 convert <url> [format]"
    echo ""
    echo "     参数:"
    echo "       url     - 飞书文档URL"
    echo "       format  - 输出格式: pdf, markdown (默认: markdown)"
    echo ""
    echo "     示例:"
    echo "       $0 convert https://xxx.feishu.cn/docx/xxx pdf"
    echo "       $0 convert https://xxx.feishu.cn/wiki/xxx markdown"
    echo ""
    echo "  2. 批量转换:"
    echo "     $0 batch <json_file> [output_dir] [format]"
    echo ""
    echo "     参数:"
    echo "       json_file  - 包含文档token的JSON文件路径"
    echo "       output_dir - 输出目录 (默认: ./batch_output)"
    echo "       format     - 输出格式: pdf, markdown (默认: markdown)"
    echo ""
    echo "     示例:"
    echo "       $0 batch get_info.json ./output markdown"
    echo "       $0 batch get_info.json ./output pdf"
    echo ""
    echo "     特性:"
    echo "       - 自动设置6秒间隔，避免触发API速率限制"
    echo "       - 默认使用文档标题作为文件名（更友好）"
    echo "       - 如需使用token作为文件名，添加 --use-token-filename 参数"
    echo ""
    echo "  3. 测试转换:"
    echo "     $0 test"
    echo "     创建 Demo 文档并测试转换功能"
    echo ""
    echo "  4. 完整测试（创建+转换+比对）:"
    echo "     $0 compare"
    echo "     创建50+块类型文档，转换后比对差异"
    echo ""
    echo "  5. 创建 Demo:"
    echo "     $0 demo              # 创建基础 Demo 文档（约10种块类型）"
    echo "     $0 demo --comprehensive  # 创建完整 Demo 文档（50+块类型）"
    echo ""
    echo "  6. 环境设置:"
    echo "     $0 setup"
    echo "     创建虚拟环境并安装依赖"
    echo ""
    echo "  7. PDF转Markdown:"
    echo "     $0 pdf2md <pdf_file> [output_file]"
    echo "     将PDF文件转换为Markdown格式"
    echo ""
    echo "  8. 帮助:"
    echo "     $0 help"
    echo "     显示此帮助信息"
    echo ""
    echo "========================================"
}

# 主函数
main() {
    check_project_dir
    check_python_version
    
    case "${1:-help}" in
        "setup")
            print_info "Setting up environment..."
            create_venv
            activate_venv
            install_dependencies
            check_env_vars
            print_info "Setup completed successfully!"
            print_info "You can now run: $0 convert <url> [format]"
            print_info "Or run batch conversion: $0 batch <json_file> [output_dir] [format]"
            ;;
        "convert")
            create_venv
            activate_venv
            install_dependencies
            check_env_vars
            execute_conversion "$2" "$3"
            ;;
        "batch")
            create_venv
            activate_venv
            install_dependencies
            check_env_vars
            execute_batch_conversion "$2" "$3" "$4"
            ;;
        "test")
            create_venv
            activate_venv
            install_dependencies
            check_env_vars
            print_info "运行转换测试..."
            python test_conversion.py --output-dir ./test_output
            ;;
        "compare")
            create_venv
            activate_venv
            install_dependencies
            check_env_vars
            print_highlight "========================================"
            print_highlight "   完整测试：创建 + 转换 + 比对"
            print_highlight "========================================"
            python test_and_compare.py --output-dir ./test_comparison
            ;;
        "demo")
            create_venv
            activate_venv
            install_dependencies
            check_env_vars
            if [[ "$2" == "--comprehensive" ]]; then
                print_info "创建完整 Demo 文档（50+块类型）..."
                python -c "from feishu_converter.tools import create_comprehensive_demo_document; import os; doc_token = create_comprehensive_demo_document(); print(f'完整 Demo 文档创建成功: {doc_token}')"
            else
                print_info "创建基础 Demo 文档..."
                python -c "from feishu_converter.tools import create_demo_document; import os; doc_token = create_demo_document(); print(f'Demo 文档创建成功: {doc_token}')"
            fi
            ;;
        "pdf2md")
            create_venv
            activate_venv
            install_dependencies
            check_env_vars
            if [[ -z "$2" ]]; then
                print_error "Usage: $0 pdf2md <pdf_file> [output_file]"
                exit 1
            fi
            PDF_FILE="$2"
            OUTPUT_FILE="${3:-${PDF_FILE%.pdf}.md}"
            print_info "将PDF文件转换为Markdown: $PDF_FILE"
            print_info "输出文件: $OUTPUT_FILE"
            python -c "from feishu_converter.tools import convert_pdf_to_markdown; import os; result = convert_pdf_to_markdown('$PDF_FILE', '$OUTPUT_FILE'); print(f'PDF转Markdown成功！输出文件: $OUTPUT_FILE')"
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            print_error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# 调用主函数
main "$@"
