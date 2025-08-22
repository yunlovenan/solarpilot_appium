#!/bin/bash

echo "🔍 Jenkins环境检查脚本"
echo "====================="

# 清理代理环境变量
unset all_proxy http_proxy https_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY
echo "✅ 代理环境变量已清理"

# 检查系统信息
echo ""
echo "📋 系统信息:"
echo "操作系统: $(uname -s) $(uname -r)"
echo "架构: $(uname -m)"
echo "当前用户: $(whoami)"
echo "当前目录: $(pwd)"

# 检查环境变量
echo ""
echo "🔧 环境变量:"
echo "PATH: $PATH"
echo "PYTHONPATH: ${PYTHONPATH:-未设置}"
echo "JAVA_HOME: ${JAVA_HOME:-未设置}"
echo "ANDROID_HOME: ${ANDROID_HOME:-未设置}"

# 检查关键命令
echo ""
echo "📱 关键命令检查:"
echo "Python: $(which python3 2>/dev/null || echo '未找到')"
echo "Appium: $(which appium 2>/dev/null || echo '未找到')"
echo "ADB: $(which adb 2>/dev/null || echo '未找到')"
echo "Node: $(which node 2>/dev/null || echo '未找到')"

# 检查Appium版本
if command -v appium &> /dev/null; then
    echo "Appium版本: $(appium --version)"
else
    echo "❌ Appium未安装"
fi

# 检查模拟器状态
echo ""
echo "📱 模拟器状态:"
adb devices

# 检查端口占用
echo ""
echo "🔌 端口检查:"
echo "端口4723: $(lsof -i :4723 2>/dev/null || echo '未被占用')"
echo "端口8080: $(lsof -i :8080 2>/dev/null || echo '未被占用')"

# 检查网络连接
echo ""
echo "🌐 网络连接检查:"
echo "本地Appium: $(curl -s http://localhost:4723/wd/hub/status 2>/dev/null && echo '✅ 可访问' || echo '❌ 不可访问')"
echo "GitHub: $(curl -s --connect-timeout 5 https://github.com 2>/dev/null && echo '✅ 可访问' || echo '❌ 不可访问')"

# 检查项目结构
echo ""
echo "📁 项目结构检查:"
echo "项目根目录: $PROJECT_ROOT"
echo "虚拟环境: $([ -d "venv" ] && echo '✅ 存在' || echo '❌ 不存在')"
echo "测试文件: $([ -f "testcase/test_app_01_login.py" ] && echo '✅ 存在' || echo '❌ 不存在')"

echo ""
echo "🎯 环境检查完成！"
