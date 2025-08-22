# 🚀 快速参考指南

## 📁 目录结构概览

```
Appium_Solat/
├── 📚 docs/           # 项目文档
├── 🐳 docker/         # Docker配置
├── 📜 scripts/        # 脚本文件
├── ⚙️ conf/           # 配置文件
├── 🧪 testcase/       # 测试用例
├── 📱 page/           # 页面对象
├── 🎯 locator/        # 元素定位器
├── 🔧 common/         # 公共模块
├── 📊 data/           # 测试数据
├── 🚀 jenkins/        # Jenkins配置
├── 📱 appium_local/   # Appium模块
├── 🏃 run.py          # 主运行脚本
└── 📋 .gitignore      # Git忽略文件
```

## 🚀 常用命令

### 运行测试
```bash
# 运行移动端测试
python3 run.py mobile

# 运行特定测试用例
python3 run.py mobile --test test_app_01_login.py
```

### Docker操作
```bash
# 启动Selenium容器
docker-compose -f docker/docker-compose3.yaml up -d

# 停止Selenium容器
docker-compose -f docker/docker-compose3.yaml down

# 查看容器状态
docker ps
```

### Jenkins操作
```bash
# 启动Jenkins
bash scripts/start-jenkins.sh

# 查看Jenkins状态
docker ps | grep jenkins
```

### 文件管理
```bash
# 查看项目结构
ls -la

# 查看特定目录
ls docs/
ls docker/
ls scripts/
ls conf/
```

## 📚 重要文件位置

### 配置文件
- **应用配置**: `conf/app_config.ini`
- **测试数据**: `conf/config.ini`
- **Python依赖**: `conf/requirements.txt`

### 测试用例
- **登录测试**: `testcase/test_app_01_login.py`
- **设备添加**: `testcase/test_app_02_deviceadd.py`
- **优化器添加**: `testcase/test_app_03_optimizeradd.py`
- **Selenium测试**: `testcase/test_selenium.py`

### 页面对象
- **基础页面**: `page/base_page.py`
- **登录页面**: `page/page_app_login.py`
- **设备页面**: `page/page_app_device.py`
- **优化器页面**: `page/page_app_optimizer.py`

### 元素定位器
- **设备定位器**: `locator/locator_app_device.py`
- **登录定位器**: `locator/locator_app_login.py`
- **天线定位器**: `locator/locator_antena.py`

## 🔧 环境设置

### Python环境
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r conf/requirements.txt
```

### Appium环境
```bash
# 安装Appium
npm install -g appium

# 启动Appium服务器
appium
```

### Docker环境
```bash
# 检查Docker状态
docker --version
docker-compose --version

# 启动Docker服务
open -a Docker
```

## 📊 测试报告

### Allure报告
```bash
# 生成报告
allure serve allure_report/

# 生成HTML报告
allure generate allure_report/ --clean
```

### 日志文件
- **测试日志**: `result/logs/`
- **截图**: `screenshots/`
- **下载文件**: `downloads/`

## 🚨 故障排除

### 常见问题
1. **Appium连接失败**: 检查端口4723是否被占用
2. **设备未连接**: 检查ADB设备列表
3. **元素找不到**: 检查定位器是否正确
4. **Docker启动失败**: 检查Docker服务状态

### 日志查看
```bash
# 查看Appium日志
tail -f ~/.npm/_logs/*.log

# 查看测试日志
tail -f result/logs/all.log

# 查看Docker日志
docker logs selenium-chrome
```

## 📞 获取帮助

- **项目文档**: 查看 `docs/` 目录
- **代码注释**: 查看各Python文件的注释
- **错误日志**: 查看 `result/logs/` 目录
- **测试报告**: 查看 `allure_report/` 目录
