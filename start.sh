#!/bin/bash

# 飞书文档转换器脚本
# 功能：创建虚拟环境、安装依赖、执行文档转换

set -e  # 遇到错误时终止脚本

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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

# 执行转换
execute_conversion() {
    if [[ $# -ne 3 ]]; then
        print_error "Usage: $0 convert <feishu_doc_url> <output_format> <output_path>"
        print_info "Supported formats: pdf, markdown"
        exit 1
    fi
    
    DOC_URL="$1"
    OUTPUT_FORMAT="$2"
    OUTPUT_PATH="$3"
    
    print_info "Converting document: $DOC_URL -> $OUTPUT_PATH ($OUTPUT_FORMAT)"
    
    python main.py "$DOC_URL" "$OUTPUT_FORMAT" "$OUTPUT_PATH"
    
    if [[ $? -eq 0 ]]; then
        print_info "Conversion completed successfully"
    else
        print_error "Conversion failed"
        exit 1
    fi
}

# 显示帮助信息
show_help() {
    echo "飞书文档转换器脚本"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  setup          创建虚拟环境并安装依赖"
    echo "  convert <url> <format> <path>  转换飞书文档 (支持格式: pdf, markdown)"
    echo "  run_tests      运行单元测试"
    echo "  help           显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 setup"
    echo "  $0 convert https://example.feishu.cn/docx/xxx pdf /path/to/output.pdf"
    echo "  $0 convert https://example.feishu.cn/docx/xxx markdown /path/to/output.md"
    echo "  $0 run_tests"
}

# 运行单元测试
run_tests() {
    print_info "Running unit tests"
    
    python -m pytest test_converter.py -v
    
    if [[ $? -eq 0 ]]; then
        print_info "All tests passed"
    else
        print_error "Some tests failed"
        exit 1
    fi
}

# 主函数
main() {
    check_project_dir
    check_python_version
    
    case "${1:-help}" in
        "setup")
            create_venv
            activate_venv
            install_dependencies
            check_env_vars
            print_info "Setup completed successfully"
            ;;
        "convert")
            if [[ $# -ne 4 ]]; then
                print_error "Usage: $0 convert <feishu_doc_url> <output_format> <output_path>"
                exit 1
            fi
            
            create_venv
            activate_venv
            install_dependencies
            check_env_vars
            execute_conversion "$2" "$3" "$4"
            ;;
        "run_tests")
            create_venv
            activate_venv
            install_dependencies
            run_tests
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