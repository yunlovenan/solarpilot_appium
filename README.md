# 🚀 SolarPilot Appium 自动化测试项目

## 📁 项目结构

```
Appium_Solat/
├── 📚 docs/                    # 项目文档
│   ├── README.md              # 项目说明
│   ├── GIT_DEPLOYMENT_SUMMARY.md
│   ├── JENKINS_SUMMARY.md
│   ├── DOCKER_INSTALLATION_SUMMARY.md
│   ├── GITHUB_CONNECTION_SUCCESS.md
│   └── JENKINS_DOCKER_SOLUTION.md
├── 🐳 docker/                  # Docker配置文件
│   └── docker-compose3.yaml   # Selenium Chrome容器配置
├── 📜 scripts/                 # 脚本文件
│   └── start-jenkins.sh       # Jenkins启动脚本
├── ⚙️ conf/                    # 配置文件
│   ├── app_config.ini         # 应用配置
│   ├── config.ini             # 测试数据配置
│   └── requirements.txt       # Python依赖
├── 🧪 testcase/                # 测试用例
│   ├── conftest.py            # Pytest配置
│   ├── test_app_01_login.py   # 登录测试
│   ├── test_app_02_deviceadd.py # 设备添加测试
│   ├── test_app_03_optimizeradd.py # 优化器添加测试
│   └── test_selenium.py       # Selenium测试
├── 📱 page/                    # 页面对象
│   ├── base_page.py           # 基础页面类
│   ├── page_app_login.py      # 登录页面
│   ├── page_app_login.py      # 登录页面
│   ├── page_app_device.py     # 设备页面
│   └── page_app_optimizer.py  # 优化器页面
├── 🎯 locator/                 # 元素定位器
│   ├── locator_app_device.py  # 设备页面定位器
│   ├── locator_app_login.py   # 登录页面定位器
│   └── locator_antena.py      # 天线页面定位器
├── 🔧 common/                  # 公共模块
│   ├── base_page.py           # 基础页面类
│   ├── handle_config.py       # 配置处理
│   └── handle_logging.py      # 日志处理
├── 📊 data/                    # 测试数据
│   └── case_data.py           # 测试用例数据
├── 🚀 jenkins/                 # Jenkins CI/CD配置
│   ├── Dockerfile             # Jenkins Docker镜像
│   ├── docker-compose.yml     # Jenkins服务配置
│   ├── Jenkinsfile            # Jenkins Pipeline
│   └── manage-android-vm.sh   # Android虚拟机管理
├── 📱 appium_local/            # Appium本地模块
├── 🎭 allure_report/           # Allure测试报告
├── 📝 result/                  # 测试结果和日志
├── 📥 downloads/               # 下载文件目录
├── 📸 screenshots/             # 截图目录
├── 🐍 venv/                    # Python虚拟环境
├── 🏃 run.py                   # 主运行脚本
├── 📋 .gitignore               # Git忽略文件
└── 📖 README.md                # 项目说明文档
```

## 🚀 快速开始

### 1. 环境准备
```bash
# 安装Python依赖
pip install -r conf/requirements.txt

# 启动Appium服务器
appium
```

### 2. 运行测试
```bash
# 运行移动端测试
python3 run.py mobile

# 运行特定测试用例
python3 run.py mobile --test test_app_01_login.py
```

### 3. 启动Selenium容器
```bash
# 启动Chrome容器
docker-compose -f docker/docker-compose3.yaml up -d
```

### 4. 启动Jenkins
```bash
# 启动Jenkins服务
bash scripts/start-jenkins.sh
```

## 📚 文档说明

- **docs/**: 包含所有项目文档和说明
- **docker/**: Docker相关配置文件
- **scripts/**: 各种脚本文件
- **conf/**: 配置文件和依赖列表

## 🔧 主要功能

- 📱 移动端自动化测试 (Appium + UiAutomator2)
- 🌐 Web端自动化测试 (Selenium)
- 🔄 持续集成 (Jenkins)
- 📊 测试报告 (Allure)
- 🐳 容器化部署 (Docker)

## 📞 技术支持

如有问题，请查看相关文档或联系开发团队。
