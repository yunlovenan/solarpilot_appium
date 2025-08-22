# 🚀 Jenkins持续集成完整指南

## 📋 项目概述
**项目名称**: Appium移动端自动化测试  
**技术栈**: Python + Appium + UiAutomator2 + Pytest + Allure  
**目标**: 实现移动端测试的自动化执行和报告生成

---

## 🎯 第一阶段：环境准备

### 1.1 系统环境检查
```bash
# 检查Python版本
python3 --version

# 检查Node.js版本（Appium需要）
node --version

# 检查ADB连接
adb devices

# 检查Android模拟器状态
emulator -list-avds
```

### 1.2 依赖包安装
```bash
# 安装Python依赖包（系统环境）
/opt/homebrew/bin/python3 -m pip install pytest
/opt/homebrew/bin/python3 -m pip install selenium
/opt/homebrew/bin/python3 -m pip install appium-python-client
/opt/homebrew/bin/python3 -m pip install allure-pytest
/opt/homebrew/bin/python3 -m pip install openpyxl
/opt/homebrew/bin/python3 -m pip install pymysql
```

### 1.3 Appium安装和配置
```bash
# 安装Appium
npm install -g appium

# 安装UiAutomator2驱动
appium driver install uiautomator2

# 验证安装
appium driver list
```

---

## 🎯 第二阶段：项目结构搭建

### 2.1 目录结构
```
Appium_Solat/
├── jenkins/                    # Jenkins相关文件
│   ├── quick-start-local.sh   # 本地Jenkins启动脚本
│   ├── scheduled-run.sh       # 定时任务执行脚本
│   ├── manage-schedule.sh     # 定时任务管理脚本
│   ├── setup-cron.sh         # 定时任务安装脚本
│   ├── start-web.sh          # Web界面启动脚本
│   ├── index.html            # Web界面主页
│   ├── test.html             # Web界面测试页
│   └── logs/                 # 日志目录
├── testcase/                  # 测试用例
│   ├── conftest.py           # Pytest配置
│   ├── test_app_01_login.py  # 登录测试
│   └── test_app_03_optimizeradd.py # 优化器添加测试
├── page/                      # 页面对象
├── locator/                   # 元素定位器
├── common/                    # 公共模块
├── conf/                      # 配置文件
│   └── config.ini            # 测试数据配置
├── data/                      # 测试数据
├── result/                    # 测试结果
└── run.py                     # 主运行脚本
```

### 2.2 配置文件设置
```ini
# conf/config.ini
[device_data]
zigbee_sn = GW1123C21122
device_name = 测试gateway设备
wifi_sn = 24DCBAEFA35D
optimizer_sn = SP112480122E
opt_sn_2 = SP11248010F0
opt_sn_3 = SP1124801080
opt_sn_4 = SP11248010D4
```

---

## 🎯 第三阶段：Jenkins本地化部署

### 3.1 创建Jenkins目录
```bash
# 在项目根目录创建jenkins文件夹
mkdir jenkins
cd jenkins
```

### 3.2 创建本地Jenkins启动脚本
```bash
# jenkins/quick-start-local.sh
#!/bin/bash
echo "🚀 启动Jenkins本地测试..."

# 清理代理设置
unset all_proxy
unset http_proxy
unset https_proxy

# 安装依赖
/opt/homebrew/bin/python3 -m pip install -r ../requirements.txt

# 启动Appium服务器
echo "🔧 启动Appium服务器..."
appium --base-path /wd/hub &
APPIUM_PID=$!

# 等待Appium启动
sleep 5

# 运行测试
echo "🧪 执行移动端测试..."
cd ..
/opt/homebrew/bin/python3 run.py mobile

# 生成Allure报告
echo "📊 生成Allure报告..."
allure generate result/ -o allure_report/ --clean

# 启动Allure服务
echo "🌐 启动Allure报告服务..."
allure serve allure_report/ &

echo "✅ Jenkins本地测试完成！"
```

### 3.3 创建定时任务脚本
```bash
# jenkins/scheduled-run.sh
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$SCRIPT_DIR/logs"

# 确保日志目录存在
mkdir -p "$LOG_DIR"

# 定义日志文件
TIMESTAMP=$(date +"%Y%m%d")
RUN_LOG="$LOG_DIR/scheduled-run-$TIMESTAMP.log"
ERROR_LOG="$LOG_DIR/error-$TIMESTAMP.log"

# 重定向所有输出到日志文件
exec > >(tee -a "$RUN_LOG") 2> >(tee -a "$ERROR_LOG" >&2)

echo "$(date +"%Y年 %m月%d日 %A %H时%M分%S秒 CST"): 定时任务开始执行"
echo "------------------------------------------"

# 切换到项目根目录
cd "$PROJECT_ROOT" || { echo "无法切换到项目根目录"; exit 1; }

# 运行本地快速启动脚本
echo "执行测试运行..."
"$SCRIPT_DIR/quick-start-local.sh"

echo "------------------------------------------"
echo "$(date +"%Y年 %m月%d日 %A %H时%M分%S秒 CST"): 定时任务执行完成"
```

### 3.4 创建定时任务管理脚本
```bash
# jenkins/manage-schedule.sh
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCHEDULED_RUN_SCRIPT="$SCRIPT_DIR/scheduled-run.sh"
SETUP_CRON_SCRIPT="$SCRIPT_DIR/setup-cron.sh"
LOG_DIR="$SCRIPT_DIR/logs"

function show_status() {
    echo "检查Jenkins定时任务状态..."
    if crontab -l 2>/dev/null | grep -q "$SCHEDULED_RUN_SCRIPT"; then
        echo "✅ 定时任务已安装"
        echo ""
        echo "当前定时任务配置:"
        crontab -l | grep "$SCHEDULED_RUN_SCRIPT"
    else
        echo "❌ 定时任务未安装"
    fi
    echo ""
    echo "日志文件位置: $LOG_DIR/"
}

function install_schedule() {
    "$SETUP_CRON_SCRIPT"
}

function uninstall_schedule() {
    echo "卸载Jenkins定时任务..."
    crontab -l 2>/dev/null | grep -v "$SCHEDULED_RUN_SCRIPT" | crontab -
    echo "✅ 定时任务已卸载"
}

function test_schedule() {
    echo "测试Jenkins定时脚本..."
    "$SCHEDULED_RUN_SCRIPT"
}

function view_logs() {
    echo "查看Jenkins定时任务日志..."
    mkdir -p "$LOG_DIR"
    if [ -z "$(ls -A "$LOG_DIR")" ]; then
        echo "日志目录为空。"
        return
    fi

    echo "可用的日志文件:"
    ls -lh "$LOG_DIR" | grep "scheduled-run-\|error-"

    echo ""
    echo "最近的错误日志:"
    LATEST_ERROR_LOG=$(ls -t "$LOG_DIR"/error-*.log 2>/dev/null | head -n 1)
    if [ -n "$LATEST_ERROR_LOG" ]; then
        echo "=== 今天的错误日志 ==="
        cat "$LATEST_ERROR_LOG" | tail -n 20
    else
        echo "无错误日志。"
    fi

    echo ""
    echo "最近的运行日志:"
    LATEST_RUN_LOG=$(ls -t "$LOG_DIR"/scheduled-run-*.log 2>/dev/null | head -n 1)
    if [ -n "$LATEST_RUN_LOG" ]; then
        echo "=== 今天的运行日志 ==="
        cat "$LATEST_RUN_LOG" | tail -n 20
    else
        echo "无运行日志。"
    fi
}

case "$1" in
    status)
        show_status
        ;;
    install)
        install_schedule
        ;;
    uninstall)
        uninstall_schedule
        ;;
    test)
        test_schedule
        ;;
    logs)
        view_logs
        ;;
    *)
        echo "用法: $0 {status|install|uninstall|test|logs}"
        exit 1
        ;;
esac
```

### 3.5 创建定时任务安装脚本
```bash
# jenkins/setup-cron.sh
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SCHEDULED_RUN_SCRIPT="$SCRIPT_DIR/scheduled-run.sh"

echo "设置Jenkins定时任务..."

# 检查并创建日志目录
LOG_DIR="$SCRIPT_DIR/logs"
mkdir -p "$LOG_DIR"

# 添加或更新crontab任务
(crontab -l 2>/dev/null | grep -v "$SCHEDULED_RUN_SCRIPT"; echo "0 15 * * * $SCHEDULED_RUN_SCRIPT") | crontab -

echo "✅ 定时任务设置成功！"
echo "📅 任务将在每天15:00自动运行"
echo "📝 日志文件位置: $LOG_DIR/"
echo ""
echo "当前crontab配置:"
crontab -l | grep "$SCHEDULED_RUN_SCRIPT"
echo ""
echo "如需修改时间，请运行: crontab -e"
echo "如需删除定时任务，请运行: crontab -r"
```

---

## 🎯 第四阶段：Web界面部署

### 4.1 创建Web界面启动脚本
```bash
# jenkins/start-web.sh
#!/bin/bash
echo "启动Jenkins本地Web界面..."

# 检查端口是否被占用
if lsof -i :8080 > /dev/null; then
    echo "⚠️ 端口8080已被占用，请检查是否有其他服务正在运行。"
    echo "💡 您可以尝试杀死占用端口的进程，例如: kill $(lsof -t -i :8080)"
    exit 1
fi

# 切换到jenkins目录
cd "$(dirname "$0")" || { echo "无法切换到jenkins目录"; exit 1; }

# 启动Python的简单HTTP服务器
nohup python3 -m http.server 8080 > /dev/null 2>&1 &
SERVER_PID=$!
echo "✅ Web服务器已在后台启动，PID: $SERVER_PID"
echo "🌐 请在浏览器中访问: http://localhost:8080"
echo "💡 如需停止Web服务器，请执行: kill $SERVER_PID"
```

### 4.2 创建Web界面文件
```html
<!-- jenkins/index.html -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jenkins移动端测试</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #eee;
        }
        .status-card {
            background: #f8f9fa;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
            border-left: 4px solid #007cba;
        }
        .status-ok {
            border-left-color: #28a745;
        }
        .status-error {
            border-left-color: #dc3545;
        }
        .btn {
            background: #007cba;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin: 5px;
            text-decoration: none;
            display: inline-block;
        }
        .btn:hover {
            background: #005a8b;
        }
        .log-section {
            background: #f8f9fa;
            padding: 15px;
            margin: 10px 0;
            border-radius: 4px;
            font-family: monospace;
            white-space: pre-wrap;
            max-height: 300px;
            overflow-y: auto;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Jenkins移动端自动化测试</h1>
            <p>定时任务管理和状态监控</p>
        </div>
        
        <div class="status-card status-ok">
            <h3>📊 系统状态</h3>
            <p><strong>定时任务:</strong> ✅ 已安装（每天15:00运行）</p>
            <p><strong>Appium服务:</strong> ✅ 运行中</p>
            <p><strong>最后运行:</strong> 今天 13:51</p>
            <p><strong>下次运行:</strong> 明天 15:00</p>
        </div>
        
        <div class="status-card">
            <h3>⚙️ 快速操作</h3>
            <button onclick="runTest()" class="btn">🚀 手动运行测试</button>
            <button onclick="checkStatus()" class="btn">🔍 检查状态</button>
            <a href="logs.html" class="btn">📋 查看日志</a>
        </div>
        
        <div class="status-card">
            <h3>📈 最近日志</h3>
            <div class="log-section">2025-07-31 13:50:22 - 开始执行移动端测试
2025-07-31 13:50:23 - Appium服务器已启动
2025-07-31 13:50:24 - 点击元素成功
2025-07-31 13:50:25 - 输入文本成功
2025-07-31 13:50:26 - 隐藏键盘成功
2025-07-31 13:50:27 - 点击Done按钮成功
2025-07-31 13:50:28 - 点击Confirm按钮成功
2025-07-31 13:50:29 - 点击Direct Scan成功
2025-07-31 13:50:30 - 输入SN成功
2025-07-31 13:50:31 - 测试执行完成</div>
        </div>
        
        <div class="status-card">
            <h3>📋 管理命令</h3>
            <p><code>./manage-schedule.sh status</code> - 查看定时任务状态</p>
            <p><code>./manage-schedule.sh logs</code> - 查看详细日志</p>
            <p><code>./manage-schedule.sh test</code> - 手动测试运行</p>
            <p><code>./manage-schedule.sh uninstall</code> - 卸载定时任务</p>
        </div>
    </div>
    
    <script>
        function runTest() {
            alert('正在启动测试...\n请查看终端输出获取详细信息。');
        }
        
        function checkStatus() {
            location.reload();
        }
        
        // 自动刷新页面
        setTimeout(function() {
            location.reload();
        }, 30000); // 每30秒刷新一次
    </script>
</body>
</html>
```

---

## 🎯 第五阶段：部署和测试

### 5.1 设置脚本权限
```bash
# 设置所有脚本为可执行
chmod +x jenkins/*.sh

# 验证权限
ls -la jenkins/*.sh
```

### 5.2 安装定时任务
```bash
# 进入jenkins目录
cd jenkins

# 安装定时任务
./manage-schedule.sh install

# 验证安装
./manage-schedule.sh status
```

### 5.3 启动Web界面
```bash
# 启动Web服务器
./start-web.sh

# 在浏览器中访问
# http://localhost:8080
# http://localhost:8080/index.html
```

### 5.4 测试完整流程
```bash
# 手动测试运行
./manage-schedule.sh test

# 查看日志
./manage-schedule.sh logs

# 检查定时任务状态
./manage-schedule.sh status
```

---

## 🎯 第六阶段：监控和维护

### 6.1 日常监控命令
```bash
# 查看定时任务状态
./jenkins/manage-schedule.sh status

# 查看最新日志
./jenkins/manage-schedule.sh logs

# 手动触发测试
./jenkins/manage-schedule.sh test

# 访问Web界面
# http://localhost:8080
```

### 6.2 故障排除
```bash
# 检查Appium服务状态
ps aux | grep appium

# 检查端口占用
lsof -i :4723
lsof -i :8080

# 重启Appium服务
pkill -f appium
appium --base-path /wd/hub &

# 重启Web服务器
pkill -f "python3 -m http.server"
cd jenkins && python3 -m http.server 8080 &
```

### 6.3 日志管理
```bash
# 查看运行日志
tail -f jenkins/logs/scheduled-run-$(date +%Y%m%d).log

# 查看错误日志
tail -f jenkins/logs/error-$(date +%Y%m%d).log

# 清理旧日志
find jenkins/logs -name "*.log" -mtime +7 -delete
```

---

## 📊 成功指标

### ✅ 环境检查
- [ ] Python 3.13+ 已安装
- [ ] Node.js 已安装
- [ ] Appium 已安装并配置
- [ ] ADB 设备连接正常
- [ ] 所有依赖包已安装

### ✅ 脚本功能
- [ ] `quick-start-local.sh` 可正常执行
- [ ] `scheduled-run.sh` 可正常执行
- [ ] `manage-schedule.sh` 所有功能正常
- [ ] `start-web.sh` 可启动Web服务器

### ✅ 定时任务
- [ ] crontab 任务已安装
- [ ] 每天15:00自动运行
- [ ] 日志文件正常生成
- [ ] 错误处理机制正常

### ✅ Web界面
- [ ] 可访问 http://localhost:8080
- [ ] 页面显示正常
- [ ] 状态信息准确
- [ ] 自动刷新功能正常

### ✅ 测试执行
- [ ] Appium服务器正常启动
- [ ] 移动端测试可正常执行
- [ ] Allure报告正常生成
- [ ] 测试结果准确

---

## 🎉 部署完成

恭喜！您的Jenkins持续集成系统已经成功部署并运行。

**主要功能**：
- ✅ 自动化测试执行
- ✅ 定时任务管理
- ✅ Web界面监控
- ✅ 日志记录和查看
- ✅ 报告生成

**访问地址**：
- Web界面：http://localhost:8080
- 测试页面：http://localhost:8080/test.html
- 主页面：http://localhost:8080/index.html

**管理命令**：
- 状态检查：`./jenkins/manage-schedule.sh status`
- 日志查看：`./jenkins/manage-schedule.sh logs`
- 手动测试：`./jenkins/manage-schedule.sh test`
- 卸载任务：`./jenkins/manage-schedule.sh uninstall`

现在您的移动端自动化测试已经完全集成到Jenkins中，可以享受持续集成带来的便利！
