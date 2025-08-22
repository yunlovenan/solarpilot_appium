#!/bin/bash

echo "🔍 Jenkins环境版本检查脚本"
echo "=========================="

# 清理代理环境变量
unset all_proxy http_proxy https_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY
echo "✅ 代理环境变量已清理"

# 激活虚拟环境
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "虚拟环境已激活"
else
    echo "❌ 虚拟环境不存在"
    exit 1
fi

echo ""
echo "📋 当前环境信息:"
echo "Python版本: $(python --version)"
echo "pip版本: $(pip --version)"
echo "当前目录: $(pwd)"

echo ""
echo "📦 关键包版本检查:"
echo "=================="

# 检查pytest版本
PYTEST_VERSION=$(pip show pytest | grep Version | awk '{print $2}')
echo "pytest: $PYTEST_VERSION"
if [[ "$PYTEST_VERSION" == 8.* ]]; then
    echo "⚠️  警告: pytest $PYTEST_VERSION 可能与Allure不兼容"
    echo "💡 建议: 使用 pytest<8.0 版本"
else
    echo "✅ pytest版本兼容"
fi

# 检查allure-pytest版本
ALLURE_VERSION=$(pip show allure-pytest | grep Version | awk '{print $2}')
echo "allure-pytest: $ALLURE_VERSION"

# 检查pluggy版本
PLUGGY_VERSION=$(pip show pluggy | grep Version | awk '{print $2}')
echo "pluggy: $PLUGGY_VERSION"

# 检查其他关键包
echo ""
echo "🔧 其他关键包:"
echo "selenium: $(pip show selenium | grep Version | awk '{print $2}')"
echo "appium-python-client: $(pip show appium-python-client | grep Version | awk '{print $2}')"

echo ""
echo "📁 项目文件检查:"
echo "=================="
echo "requirements.txt: $([ -f "requirements.txt" ] && echo "✅ 存在" || echo "❌ 不存在")"
echo "jenkins/requirements-jenkins.txt: $([ -f "jenkins/requirements-jenkins.txt" ] && echo "✅ 存在" || echo "❌ 不存在")"

echo ""
echo "🎯 版本兼容性建议:"
echo "=================="
if [[ "$PYTEST_VERSION" == 8.* ]]; then
    echo "1. 立即降级pytest: pip install 'pytest<8.0' --force-reinstall"
    echo "2. 使用Jenkins专用requirements: pip install -r jenkins/requirements-jenkins.txt"
    echo "3. 验证版本: pytest --version"
fi

echo ""
echo "🎉 版本检查完成！"
