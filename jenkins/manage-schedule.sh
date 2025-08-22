#!/bin/bash

# Jenkins定时任务管理脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCHEDULED_SCRIPT="$SCRIPT_DIR/scheduled-run.sh"
SETUP_SCRIPT="$SCRIPT_DIR/setup-cron.sh"

show_help() {
    echo "Jenkins定时任务管理脚本"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  install    安装定时任务（每天15:00运行）"
    echo "  uninstall  卸载定时任务"
    echo "  status     查看定时任务状态"
    echo "  logs       查看最近的日志"
    echo "  test       测试定时脚本"
    echo "  help       显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 install    # 安装定时任务"
    echo "  $0 status     # 查看状态"
    echo "  $0 logs       # 查看日志"
}

install_schedule() {
    echo "安装Jenkins定时任务..."
    if [ -f "$SETUP_SCRIPT" ]; then
        bash "$SETUP_SCRIPT"
    else
        echo "错误：找不到设置脚本 $SETUP_SCRIPT"
        exit 1
    fi
}

uninstall_schedule() {
    echo "卸载Jenkins定时任务..."
    
    # 创建临时crontab文件
    TEMP_CRON=$(mktemp)
    
    # 导出当前crontab并过滤掉Jenkins相关任务
    crontab -l > "$TEMP_CRON" 2>/dev/null || echo "" > "$TEMP_CRON"
    sed -i '' '/scheduled-run.sh/d' "$TEMP_CRON"
    sed -i '' '/Jenkins移动端测试定时任务/d' "$TEMP_CRON"
    
    # 安装更新后的crontab
    crontab "$TEMP_CRON"
    
    # 清理临时文件
    rm "$TEMP_CRON"
    
    echo "✅ 定时任务已卸载"
}

check_status() {
    echo "检查Jenkins定时任务状态..."
    echo ""
    
    # 检查crontab中是否有Jenkins任务
    if crontab -l 2>/dev/null | grep -q "scheduled-run.sh"; then
        echo "✅ 定时任务已安装"
        echo ""
        echo "当前定时任务配置:"
        crontab -l | grep -A 2 -B 2 "scheduled-run.sh"
    else
        echo "❌ 定时任务未安装"
    fi
    
    echo ""
    echo "日志文件位置: $SCRIPT_DIR/logs/"
    
    # 检查最近的日志文件
    if [ -d "$SCRIPT_DIR/logs" ]; then
        echo ""
        echo "最近的日志文件:"
        ls -la "$SCRIPT_DIR/logs/" | head -5
    fi
}

show_logs() {
    echo "查看Jenkins定时任务日志..."
    echo ""
    
    LOG_DIR="$SCRIPT_DIR/logs"
    
    if [ ! -d "$LOG_DIR" ]; then
        echo "日志目录不存在: $LOG_DIR"
        return
    fi
    
    # 显示最近的日志文件
    echo "可用的日志文件:"
    ls -la "$LOG_DIR/" | grep "\.log$"
    
    echo ""
    echo "最近的错误日志:"
    if [ -f "$LOG_DIR/error-$(date +%Y%m%d).log" ]; then
        echo "=== 今天的错误日志 ==="
        tail -20 "$LOG_DIR/error-$(date +%Y%m%d).log"
    else
        echo "今天没有错误日志"
    fi
    
    echo ""
    echo "最近的运行日志:"
    if [ -f "$LOG_DIR/scheduled-run-$(date +%Y%m%d).log" ]; then
        echo "=== 今天的运行日志 ==="
        tail -20 "$LOG_DIR/scheduled-run-$(date +%Y%m%d).log"
    else
        echo "今天没有运行日志"
    fi
}

test_schedule() {
    echo "测试Jenkins定时脚本..."
    echo ""
    
    if [ -f "$SCHEDULED_SCRIPT" ]; then
        echo "执行测试运行..."
        bash "$SCHEDULED_SCRIPT"
    else
        echo "错误：找不到定时脚本 $SCHEDULED_SCRIPT"
        exit 1
    fi
}

# 主程序
case "${1:-help}" in
    install)
        install_schedule
        ;;
    uninstall)
        uninstall_schedule
        ;;
    status)
        check_status
        ;;
    logs)
        show_logs
        ;;
    test)
        test_schedule
        ;;
    help|*)
        show_help
        ;;
esac
