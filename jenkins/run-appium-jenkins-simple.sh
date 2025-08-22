#!/bin/bash

echo "🚀 Jenkins Appium简化测试脚本"
echo "============================="

# 清理代理环境变量
unset all_proxy http_proxy https_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY

# 设置环境变量
export PROJECT_ROOT="/Users/mayun/project/solarpilot/Appium_Solat"
export APPIUM_URL="http://localhost:4723/wd/hub"

echo "项目根目录: $PROJECT_ROOT"
echo "Appium URL: $APPIUM_URL"

# 切换到项目根目录
cd "$PROJECT_ROOT" || exit 1

# 检查模拟器状态
echo "检查模拟器状态..."
adb devices

# 检查Appium服务器状态
echo "检查Appium服务器状态..."
if curl -s "$APPIUM_URL/status" > /dev/null 2>&1; then
    echo "✅ Appium服务器正在运行"
else
    echo "❌ Appium服务器未运行，尝试启动..."
    
    # 停止现有进程
    pkill -f "appium.*server" 2>/dev/null
    pkill -f "appium.*--base-path" 2>/dev/null
    sleep 3
    
    # 启动Appium
    APPIUM_VERSION=$(appium --version)
    echo "Appium版本: $APPIUM_VERSION"
    
    if [[ $APPIUM_VERSION == 2.* ]]; then
        nohup appium server --base-path /wd/hub --port 4723 --log-level debug > appium.log 2>&1 &
    else
        nohup appium --base-path /wd/hub --log-level debug > appium.log 2>&1 &
    fi
    
    appium_pid=$!
    echo "Appium进程ID: $appium_pid"
    
    # 等待启动
    echo "等待Appium启动..."
    for i in {1..45}; do
        if curl -s "$APPIUM_URL/status" > /dev/null 2>&1; then
            echo "✅ Appium启动成功"
            break
        fi
        
        if ! kill -0 $appium_pid 2>/dev/null; then
            echo "❌ Appium进程退出"
            tail -20 appium.log
            exit 1
        fi
        
        sleep 2
        echo "等待中... ($i/45)"
    done
fi

# 激活虚拟环境
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "虚拟环境已激活"
else
    echo "❌ 虚拟环境不存在"
    exit 1
fi

# 创建目录
mkdir -p result/logs result/screenshots result/reports

# 运行测试（生成Allure结果和JUnit报告）
echo "运行测试..."
pytest testcase/test_app_01_login.py -v --alluredir=ALLURE-RESULTS --junitxml=junit.xml --tb=short
# 检查测试结果
if [ $? -eq 0 ]; then
    echo "✅ 测试执行成功"
else
    echo "⚠️ 测试执行有错误，但继续生成报告"
fi

# 生成Allure报告
echo "生成Allure报告..."
if [ -d "ALLURE-RESULTS" ] && [ "$(ls -A ALLURE-RESULTS)" ]; then
    if command -v allure &> /dev/null; then
        allure generate ALLURE-RESULTS --clean -o allure_report
        echo "✅ Allure报告已生成到 allure_report/ 目录"
    else
        echo "⚠️ allure命令不可用，跳过Allure报告生成"
        echo "Allure结果已保存到 ALLURE-RESULTS/ 目录"
    fi
else
    echo "⚠️ 没有找到Allure测试结果"
fi

# 生成简单报告
echo "生成测试报告..."
if [ -f "junit.xml" ]; then
    echo "✅ JUnit XML报告已生成"
    echo "报告位置: $(pwd)/junit.xml"
else
    echo "⚠️ JUnit XML报告生成失败"
fi

echo "🎉 Jenkins测试完成！"
