# SolarPilot移动端自动化测试项目

## 🚀 项目简介

这是一个基于Appium的移动端自动化测试项目，集成了Jenkins持续集成系统，提供完整的移动端自动化测试解决方案。

### 📋 主要功能
- **移动端自动化测试**: 使用Appium + UiAutomator2进行Android应用测试
- **Jenkins CI/CD**: 本地化部署的持续集成系统
- **定时任务**: 支持定时运行测试用例
- **Web界面**: 提供可视化的管理和监控界面
- **详细文档**: 包含完整的部署、操作和故障排除指南

### 🔧 技术栈
- **Appium**: 移动端自动化测试框架
- **Python**: 主要开发语言
- **Jenkins**: 持续集成服务器
- **Allure**: 测试报告生成工具
- **Pytest**: Python测试框架
- **UiAutomator2**: Android自动化引擎

### 📁 项目结构
```
solarpilot_git/
├── jenkins/                    # Jenkins CI/CD配置
│   ├── quick-start-local.sh   # 本地Jenkins启动脚本
│   ├── manage-schedule.sh     # 定时任务管理
│   ├── start-web.sh          # Web界面启动
│   └── *.md                  # 详细文档
├── testcase/                  # 测试用例
│   ├── test_app_01_login.py  # 登录测试
│   ├── test_app_02_deviceadd.py # 设备添加测试
│   └── test_app_03_optimizeradd.py # 优化器添加测试
├── page/                      # 页面对象
├── locator/                   # 元素定位器
├── common/                    # 公共模块
├── conf/                      # 配置文件
├── data/                      # 测试数据
└── run.py                     # 主运行脚本
```

### 🎯 核心特性
1. **完整的CI/CD流程**: 从代码到部署的完整自动化
2. **本地化部署**: 不依赖Docker，直接在系统环境运行
3. **智能错误处理**: 完善的异常处理和重试机制
4. **详细文档**: 包含部署、操作、故障排除等完整文档
5. **Web界面**: 提供可视化的管理和监控界面

### 📞 快速开始

#### 1. 克隆项目
```bash
git clone git@github.com:yunlovenan/solarpilot_git.git
cd solarpilot_git
```

#### 2. 安装依赖
```bash
pip install -r requirements.txt
```

#### 3. 启动Jenkins
```bash
./jenkins/quick-start-local.sh
```

#### 4. 访问Web界面
```bash
./jenkins/start-web.sh
# 然后访问 http://localhost:8080
```

#### 5. 运行测试
```bash
python3 run.py mobile
```

### 🔧 配置说明

#### 环境要求
- Python 3.8+
- Android SDK
- Appium 2.x
- Jenkins (可选)

#### 配置文件
- `conf/config.ini`: 主要配置文件
- `conf/app_config.ini`: 应用配置

### 📊 测试用例

#### 移动端测试
- **登录测试**: 完整的用户登录流程
- **设备添加**: 网关设备添加测试
- **优化器添加**: 优化器设备添加测试

#### Web端测试
- **站点管理**: 站点添加、编辑、删除
- **设备管理**: 设备添加、删除
- **天线管理**: 天线添加、编辑、删除

### 🎉 项目亮点
- **完整的移动端自动化测试解决方案**
- **本地化Jenkins部署，无需Docker**
- **详细的文档和操作指南**
- **智能的错误处理和重试机制**
- **可视化的Web管理界面**
- **支持定时任务和持续集成**

### 📞 联系方式
- **GitHub**: https://github.com/yunlovenan/solarpilot_git
- **文档**: 查看项目中的详细文档

### 📄 许可证
本项目采用MIT许可证，详见LICENSE文件。

## 🔄 最新更新

### 2025-08-04 更新内容
- ✅ 修复了Appium连接URL问题
- ✅ 优化了移动端测试框架
- ✅ 完善了Jenkins集成文档
- ✅ 添加了Docker解决方案文档
- ✅ 更新了测试用例和页面对象
