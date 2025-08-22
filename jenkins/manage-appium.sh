#!/bin/bash

# Appium服务器管理脚本
# 支持Appium 2.x版本

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目配置
PROJECT_ROOT="/Users/mayun/project/solarpilot/Appium_Solat"
APPIUM_LOG="$PROJECT_ROOT/appium.log"
APPIUM_URL="http://localhost:4723/wd/hub"

# 打印函数
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 检查Appium是否已安装
check_appium_installed() {
    if ! command -v appium &> /dev/null; then
        print_error "Appium未安装，请先安装Appium"
        exit 1
    fi
    
    local version=$(appium --version)
    print_info "检测到Appium版本: $version"
    
    # 检查是否为Appium 2.x
    if [[ $version == 2.* ]]; then
        print_info "使用Appium 2.x启动命令"
        APPIUM_CMD="appium server"
    else
        print_info "使用Appium 1.x启动命令"
        APPIUM_CMD="appium"
    fi
}

# 检查Appium状态
check_status() {
    if curl -s "$APPIUM_URL/status" > /dev/null 2>&1; then
        print_success "Appium服务器正在运行"
        print_info "状态URL: $APPIUM_URL/status"
        
        # 显示进程信息
        local pids=$(pgrep -f "appium.*server\|appium.*--base-path")
        if [ -n "$pids" ]; then
            print_info "Appium进程ID: $pids"
        fi
        
        # 显示端口信息
        local port_info=$(lsof -i :4723 2>/dev/null)
        if [ -n "$port_info" ]; then
            print_info "端口占用情况:"
            echo "$port_info"
        fi
    else
        print_warning "Appium服务器未运行"
        
        # 检查是否有残留进程
        local pids=$(pgrep -f "appium.*server\|appium.*--base-path")
        if [ -n "$pids" ]; then
            print_warning "发现残留的Appium进程: $pids"
        fi
    fi
}

# 启动Appium服务器
start_appium() {
    print_info "启动Appium服务器..."
    
    # 检查Appium安装
    check_appium_installed
    
    cd "$PROJECT_ROOT" || {
        print_error "无法切换到项目根目录: $PROJECT_ROOT"
        exit 1
    }
    
    if pgrep -f "appium.*server" > /dev/null || pgrep -f "appium.*--base-path" > /dev/null; then
        print_warning "发现已有Appium进程，正在停止..."
        pkill -f "appium.*server" 2>/dev/null
        pkill -f "appium.*--base-path" 2>/dev/null
        sleep 3
    fi
    
    # 根据版本选择启动命令
    if [[ $APPIUM_CMD == "appium server" ]]; then
        nohup $APPIUM_CMD --base-path /wd/hub --port 4723 --log-level debug > "$APPIUM_LOG" 2>&1 &
    else
        nohup $APPIUM_CMD --base-path /wd/hub --log-level debug > "$APPIUM_LOG" 2>&1 &
    fi
    
    appium_pid=$!
    print_info "Appium进程ID: $appium_pid"
    
    print_info "等待Appium服务器启动..."
    for i in {1..30}; do
        echo "   检查Appium状态... ($i/30)"
        if ! kill -0 $appium_pid 2>/dev/null; then
            print_error "Appium进程已退出"
            print_info "Appium日志:"
            tail -20 "$APPIUM_LOG"
            exit 1
        fi
        if curl -s "$APPIUM_URL/status" > /dev/null 2>&1; then
            print_success "Appium服务器启动成功 (PID: $appium_pid)"
            check_status
            return 0
        fi
        sleep 2
    done
    
    print_error "Appium服务器启动失败"
    print_info "Appium进程状态:"
    ps aux | grep appium
    print_info "Appium日志:"
    tail -30 "$APPIUM_LOG"
    print_info "端口占用情况:"
    lsof -i :4723 2>/dev/null || echo "端口4723未被占用"
    exit 1
}

# 停止Appium
stop_appium() {
    print_info "停止Appium服务器..."
    
    if pgrep -f "appium.*server" > /dev/null || pgrep -f "appium.*--base-path" > /dev/null; then
        pkill -f "appium.*server" 2>/dev/null
        pkill -f "appium.*--base-path" 2>/dev/null
        sleep 2
        print_success "Appium服务器已停止"
    else
        print_warning "没有发现运行中的Appium进程"
    fi
}

# 重启Appium
restart_appium() {
    print_info "重启Appium服务器..."
    stop_appium
    sleep 2
    start_appium
}

# 显示日志
show_logs() {
    if [ -f "$APPIUM_LOG" ]; then
        print_info "Appium日志 (最后50行):"
        tail -50 "$APPIUM_LOG"
    else
        print_warning "Appium日志文件不存在: $APPIUM_LOG"
    fi
}

# 主函数
main() {
    case "${1:-status}" in
        start)
            start_appium
            ;;
        stop)
            stop_appium
            ;;
        restart)
            restart_appium
            ;;
        status)
            check_status
            ;;
        logs)
            show_logs
            ;;
        *)
            echo "用法: $0 [start|stop|status|restart|logs]"
            echo ""
            echo "命令:"
            echo "  start   - 启动Appium服务器"
            echo "  stop    - 停止Appium服务器"
            echo "  restart - 重启Appium服务器"
            echo "  status  - 检查Appium服务器状态"
            echo "  logs    - 显示Appium日志"
            echo ""
            echo "示例:"
            echo "  $0 start    # 启动Appium"
            echo "  $0 status   # 检查状态"
            echo "  $0 logs     # 查看日志"
            ;;
    esac
}

# 执行主函数
main "$@"
