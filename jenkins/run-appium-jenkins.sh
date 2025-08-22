#!/bin/bash

echo "🚀 Jenkins Appium测试脚本"
echo "========================"

# 清理代理环境变量（Jenkins环境可能继承系统代理）
unset all_proxy http_proxy https_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY

# 设置环境变量
export PROJECT_ROOT="/Users/mayun/project/solarpilot/Appium_Solat"
export EMULATOR_NAME="emulator-5554"
export APPIUM_URL="http://localhost:4723/wd/hub"

echo "项目根目录: $PROJECT_ROOT"
echo "模拟器: $EMULATOR_NAME"
echo "Appium URL: $APPIUM_URL"
echo "代理环境变量已清理"

# 切换到项目根目录
cd "$PROJECT_ROOT" || exit 1

# 显示基本信息
echo "当前目录: $(pwd)"
echo "Python版本: $(python3 --version)"
echo "模拟器状态:"
adb devices

# 启动Appium服务器
echo "启动Appium服务器..."
if curl -s "$APPIUM_URL/status" > /dev/null 2>&1; then
    echo "✅ Appium服务器已在运行"
else
    # 停止现有进程
    echo "停止现有Appium进程..."
    pkill -f "appium.*server" 2>/dev/null
    pkill -f "appium.*--base-path" 2>/dev/null
    sleep 3
    
    # 检查Appium版本并选择启动命令
    APPIUM_VERSION=$(appium --version)
    echo "检测到Appium版本: $APPIUM_VERSION"
    
    if [[ $APPIUM_VERSION == 2.* ]]; then
        echo "使用Appium 2.x启动命令"
        nohup appium server --base-path /wd/hub --port 4723 --log-level debug > appium.log 2>&1 &
    else
        echo "使用Appium 1.x启动命令"
        nohup appium --base-path /wd/hub --log-level debug > appium.log 2>&1 &
    fi
    
    appium_pid=$!
    echo "Appium进程ID: $appium_pid"
    
    # 增加启动等待时间（Jenkins环境需要更长时间）
    echo "等待Appium启动（Jenkins环境可能需要更长时间）..."
    for i in {1..60}; do
        if curl -s "$APPIUM_URL/status" > /dev/null 2>&1; then
            echo "✅ Appium启动成功 (PID: $appium_pid)"
            break
        fi
        
        # 检查进程是否还在运行
        if ! kill -0 $appium_pid 2>/dev/null; then
            echo "❌ Appium进程已退出，检查日志..."
            tail -20 appium.log
            exit 1
        fi
        
        sleep 2
        echo "等待Appium启动... ($i/60)"
    done
    
    # 最终检查
    if ! curl -s "$APPIUM_URL/status" > /dev/null 2>&1; then
        echo "❌ Appium启动失败，显示日志和进程状态..."
        echo "Appium日志:"
        tail -30 appium.log
        echo "进程状态:"
        ps aux | grep appium
        echo "端口占用:"
        lsof -i :4723 2>/dev/null || echo "端口4723未被占用"
        exit 1
    fi
fi

# 创建目录
mkdir -p result/logs result/screenshots result/reports ALLURE-RESULTS allure_report

# 激活虚拟环境
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "虚拟环境已激活"
else
    echo "❌ 虚拟环境不存在"
    exit 1
fi

# 安装核心依赖
echo "安装核心依赖..."
# 使用Jenkins专用的requirements文件，确保版本兼容性
pip install -r jenkins/requirements-jenkins.txt -i https://mirrors.aliyun.com/pypi/simple/

# 运行测试（不使用Allure避免兼容性问题）
echo "运行测试..."
#pytest testcase/test_app_01_login.py -v --junitxml=junit.xml
pytest testcase/test_app_01_login.py  -v --alluredir=ALLURE-RESULTS --junitxml=junit.xml

# 生成简单报告（避免Allure兼容性问题）
echo "生成测试报告..."
if [ -f "junit.xml" ]; then
    echo "✅ JUnit XML报告已生成"
    # 可以在这里添加其他报告生成逻辑
else
    echo "⚠️ JUnit XML报告生成失败"
fi

echo "🎉 测试完成！"
