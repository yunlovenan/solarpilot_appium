# �� 项目结构说明

## 🎯 目录组织原则

本项目按照功能模块和文件类型进行目录组织，使项目结构更加清晰和易于维护。

## 📂 目录结构详解

### 📚 docs/ - 项目文档
存放所有项目相关的文档文件：
- `README.md` - 项目主要说明文档
- `GIT_DEPLOYMENT_SUMMARY.md` - Git部署总结
- `JENKINS_SUMMARY.md` - Jenkins配置总结
- `DOCKER_INSTALLATION_SUMMARY.md` - Docker安装总结
- `GITHUB_CONNECTION_SUCCESS.md` - GitHub连接成功记录
- `JENKINS_DOCKER_SOLUTION.md` - Jenkins Docker解决方案

### 🐳 docker/ - Docker配置
存放Docker相关的配置文件：
- `docker-compose3.yaml` - Selenium Chrome容器配置

### 📜 scripts/ - 脚本文件
存放各种可执行脚本：
- `start-jenkins.sh` - Jenkins启动脚本

### ⚙️ conf/ - 配置文件
存放项目配置和依赖文件：
- `app_config.ini` - 应用配置
- `config.ini` - 测试数据配置
- `requirements.txt` - Python依赖列表

### 🧪 testcase/ - 测试用例
存放所有测试用例文件：
- `conftest.py` - Pytest配置文件
- `test_app_01_login.py` - 登录测试用例
- `test_app_02_deviceadd.py` - 设备添加测试用例
- `test_app_03_optimizeradd.py` - 优化器添加测试用例
- `test_selenium.py` - Selenium测试用例

### 📱 page/ - 页面对象
存放页面对象模型（POM）相关文件：
- `base_page.py` - 基础页面类
- `page_app_login.py` - 登录页面对象
- `page_app_device.py` - 设备页面对象
- `page_app_optimizer.py` - 优化器页面对象

### 🎯 locator/ - 元素定位器
存放页面元素的定位器定义：
- `locator_app_device.py` - 设备页面元素定位器
- `locator_app_login.py` - 登录页面元素定位器
- `locator_antena.py` - 天线页面元素定位器

### 🔧 common/ - 公共模块
存放公共的工具类和基础类：
- `base_page.py` - 基础页面类
- `handle_config.py` - 配置处理工具
- `handle_logging.py` - 日志处理工具

### 📊 data/ - 测试数据
存放测试相关的数据文件：
- `case_data.py` - 测试用例数据

### 🚀 jenkins/ - Jenkins CI/CD
存放Jenkins相关的配置文件：
- `Dockerfile` - Jenkins Docker镜像构建文件
- `docker-compose.yml` - Jenkins服务配置
- `Jenkinsfile` - Jenkins Pipeline定义
- `manage-android-vm.sh` - Android虚拟机管理脚本

### 📱 appium_local/ - Appium本地模块
存放Appium相关的本地模块文件

### 🎭 allure_report/ - 测试报告
存放Allure生成的测试报告

### 📝 result/ - 测试结果
存放测试执行的结果和日志文件

### 📥 downloads/ - 下载文件
存放测试过程中下载的文件

### 📸 screenshots/ - 截图
存放测试过程中的截图文件

### 🐍 venv/ - Python虚拟环境
存放Python虚拟环境文件

## 🔄 文件移动记录

以下文件已从主目录移动到相应目录：

### 从主目录移动到 docs/
- `README.md` → `docs/README.md`
- `GIT_DEPLOYMENT_SUMMARY.md` → `docs/GIT_DEPLOYMENT_SUMMARY.md`
- `JENKINS_SUMMARY.md` → `docs/JENKINS_SUMMARY.md`
- `DOCKER_INSTALLATION_SUMMARY.md` → `docs/DOCKER_INSTALLATION_SUMMARY.md`
- `GITHUB_CONNECTION_SUCCESS.md` → `docs/GITHUB_CONNECTION_SUCCESS.md`
- `JENKINS_DOCKER_SOLUTION.md` → `docs/JENKINS_DOCKER_SOLUTION.md`

### 从主目录移动到 docker/
- `docker-compose3.yaml` → `docker/docker-compose3.yaml`

### 从主目录移动到 scripts/
- `start-jenkins.sh` → `scripts/scripts/start-jenkins.sh`

### 从主目录移动到 conf/
- `requirements.txt` → `conf/requirements.txt`

### 从主目录移动到 testcase/
- `test_selenium.py` → `testcase/test_selenium.py`

## 💡 使用建议

1. **新增文档**: 请将新的.md文档放在 `docs/` 目录下
2. **新增脚本**: 请将新的.sh脚本放在 `scripts/` 目录下
3. **新增配置**: 请将新的配置文件放在 `conf/` 目录下
4. **新增Docker配置**: 请将新的Docker文件放在 `docker/` 目录下
5. **保持主目录整洁**: 主目录只保留核心的Python文件和必要的配置文件

## �� 维护说明

- 定期检查各目录下的文件是否分类正确
- 新增文件时请按照功能分类放入相应目录
- 如有新的文件类型，可以创建新的目录进行分类
