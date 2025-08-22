#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import time
from common.base_page import BasePage
from common.handle_config import conf
# 清理代理环境变量
os.environ.pop('http_proxy', None)
os.environ.pop('https_proxy', None)
os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)
os.environ.pop('all_proxy', None)
os.environ.pop('ALL_PROXY', None)

try:
    from appium import webdriver
    from appium.options.android import UiAutomator2Options
    from appium.webdriver.common.appiumby import AppiumBy
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    from locator.locator_app_login import APPLoginLocator as app_loc
    print("✅ Appium模块导入成功")
except ImportError as e:
    print(f"❌ Appium模块导入失败: {e}")
    sys.exit(1)

class APPLoginPage(BasePage):
    """登录页面"""
    # 登录的url地址
   # url = conf.get('env', 'base_url') + conf.get('url', 'login_url')

    def __init__(self, driver=None):
        if driver:
            self.driver = driver
            self.wait = WebDriverWait(self.driver, 10)
        else:
            self.driver = None
            self.wait = None
            
            # 创建options
            self.options = UiAutomator2Options()
            self.options.platform_name = "Android"
            self.options.automation_name = "uiautomator2"
            self.options.device_name = "emulator-5554"
            self.options.app_package = "com.eiot6.solartest"
            self.options.app_activity = "com.eiot6.solartest/.MainActivity"
            self.options.no_reset = True  # 不重置应用状态
            # self.options.unicode_keyboard = True
            # self.options.reset_keyboard = True
            self.options.new_command_timeout = 6000
    
    def setup_driver(self):
        """初始化Appium驱动"""
        try:
            print("正在连接Appium服务器...")
            self.driver = webdriver.Remote('http://localhost:4723/wd/hub', options=self.options)
            self.wait = WebDriverWait(self.driver, 10)
            print("✅ Appium驱动初始化成功")
            return True
        except Exception as e:
            print(f"❌ Appium驱动初始化失败: {e}")
            return False

    def wait_for_page_load(self):
        """等待页面加载"""
        print("等待页面加载...")
        time.sleep(5)
        
        if self.driver:
            self.driver.implicitly_wait(10)

    
    def APP_login(self, user, pwd):
        """输入账号密码点击登录"""
        print("🚀 开始登录流程...")
        print(f"📱 用户名: {user}")
        print(f"🔒 密码: {pwd}")
        
        # 不检查登录状态，每次都执行登录流程
        print("🔍 跳过登录状态检查，直接执行登录流程")
        
        # 等待页面完全加载
        print("⏳ 等待页面加载...")
        time.sleep(5)
        print("✅ 页面加载完成")
        
        # 获取页面源码进行调试
        try:
            page_source = self.driver.page_source
            print(f"📄 页面源码长度: {len(page_source)}")
            
            # 检查页面中的关键元素
            if "EditText" in page_source:
                print("✅ 页面中包含EditText元素")
            else:
                print("❌ 页面中不包含EditText元素")
            
            if "Button" in page_source:
                print("✅ 页面中包含Button元素")
            else:
                print("❌ 页面中不包含Button元素")
            
            if "View" in page_source:
                print("✅ 页面中包含View元素")
            else:
                print("❌ 页面中不包含View元素")
            
            # 打印页面源码的前500个字符，看看页面结构
            print(f"📋 页面源码前500字符: {page_source[:500]}")
            
        except Exception as e:
            print(f"❌ 获取页面源码失败: {e}")
        
        # 第一步：处理用户协议
        print("\n📋 第一步：处理用户协议")
        if self.is_element_exist(app_loc.agree_loc):
            print("🔍 找到Agree按钮，准备点击...")
            self.click_element(app_loc.agree_loc, '登录_同意')
            print("✅ 成功点击了Agree按钮")
            time.sleep(2)  # 等待页面响应
        else:
            print("ℹ️ Agree按钮不存在，可能已经同意过了")
        
        # 第二步：等待页面稳定
        print("\n⏳ 第二步：等待页面稳定...")
        time.sleep(3)
        
        # 第三步：查找并分析输入框
        print("\n🔍 第三步：查找输入框元素")
        try:
            edit_texts = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
            print(f"📝 找到 {len(edit_texts)} 个EditText元素")
            for i, elem in enumerate(edit_texts):
                content_desc = elem.get_attribute('content-desc')
                text = elem.get_attribute('text')
                placeholder = elem.get_attribute('placeholder')
                print(f"  📱 EditText {i}: content-desc='{content_desc}', text='{text}', placeholder='{placeholder}'")
        except Exception as e:
            print(f"❌ 查找EditText元素失败: {e}")
        
        # 第四步：输入用户名
        print(f"\n👤 第四步：输入用户名 '{user}'")
        try:
            print("🔍 准备点击用户名输入框...")
            # 先点击输入框获得焦点
            username_element = self.driver.find_element(*app_loc.username_loc)
            username_element.click()
            time.sleep(1)
            print("✅ 用户名输入框获得焦点")
            
            # 清空输入框
            username_element.clear()
            time.sleep(0.5)
            print("✅ 用户名输入框已清空")
            
            # 输入用户名
            username_element.send_keys(user)
            time.sleep(1)
            print(f"✅ 用户名 '{user}' 输入成功")
            
            # 验证输入内容
            actual_text = username_element.get_attribute('text')
            print(f"📝 实际输入内容: '{actual_text}'")
            
        except Exception as e:
            print(f"❌ 用户名输入失败: {e}")
            return
        
        # 第五步：输入密码
        print(f"\n🔒 第五步：输入密码 '{pwd}'")
        try:
            print("🔍 准备点击密码输入框...")
            # 先点击输入框获得焦点
            password_element = self.driver.find_element(*app_loc.pwd_loc)
            password_element.click()
            time.sleep(1)
            print("✅ 密码输入框获得焦点")
            
            # 清空输入框
            password_element.clear()
            time.sleep(0.5)
            print("✅ 密码输入框已清空")
            
            # 输入密码
            password_element.send_keys(pwd)
            time.sleep(1)
            print(f"✅ 密码 '{pwd}' 输入成功")
            
            # 验证输入内容（密码可能不显示）
            actual_text = password_element.get_attribute('text')
            print(f"📝 密码输入框内容: {'*' * len(actual_text) if actual_text else '空'}")
            
        except Exception as e:
            print(f"❌ 密码输入失败: {e}")
            return
        
        # 第六步：处理服务条款复选框
        print("\n☑️ 第六步：处理服务条款复选框")
        checkbox_result = self.handle_service_agreement_checkbox()
        if checkbox_result:
            print("✅ 服务条款复选框处理成功")
        else:
            print("⚠️ 服务条款复选框处理失败，继续执行...")
        
        # 第七步：点击登录按钮
        print("\n🚀 第七步：点击登录按钮")
        try:
            print("🔍 查找登录按钮...")
            login_button = self.driver.find_element(*app_loc.login_loc)
            button_text = login_button.get_attribute('content-desc')
            print(f"📝 登录按钮文本: '{button_text}'")
            
            print("👆 准备点击登录按钮...")
            login_button.click()
            print("✅ 登录按钮点击成功")
            
            # 等待登录响应
            print("⏳ 等待登录响应...")
            time.sleep(5)
            
        except Exception as e:
            print(f"❌ 登录按钮点击失败: {e}")
            return
        
        # 第八步：处理服务商选择
        print("\n🏢 第八步：处理服务商选择")
        try:
            print("🔍 查找服务商按钮...")
            self.wait_for_element_exist(app_loc.me_service, 10)
            print("✅ 找到服务商按钮")
            
            service_button = self.driver.find_element(*app_loc.me_service)
            button_text = service_button.get_attribute('content-desc')
            print(f"📝 服务商按钮文本: '{button_text}'")
            
            print("👆 准备点击服务商按钮...")
            service_button.click()
            print("✅ 服务商按钮点击成功")
            
        except Exception as e:
            print(f"❌ 服务商按钮处理失败: {e}")
        
        # 第九步：处理权限弹窗
        print("\n🔐 第九步：处理权限弹窗")
        self.handle_permission_dialogs()
        
        # 第十步：保存登录状态
        print("\n💾 第十步：保存登录状态")
        self.save_mobile_login_state()
        
        # 完成
        print("\n🎉 登录流程完成！")
        time.sleep(3)
    
    def handle_service_agreement_checkbox(self):
        """处理服务条款复选框 - 使用优化的定位策略"""
        print("🔍 开始处理服务条款复选框...")
        
        # 只保留上次成功的2种定位策略
        locators = [
            app_loc.service_loc,  # 主要策略
            (AppiumBy.XPATH, "//*[contains(@content-desc, 'agree') or contains(@content-desc, 'policy') or contains(@content-desc, 'Agree') or contains(@content-desc, 'Policy')]"),  # 备用策略
        ]
        
        print(f"📋 将尝试 {len(locators)} 种定位策略")
        
        # 尝试每种定位策略
        for i, locator in enumerate(locators):
            try:
                print(f"  🔍 尝试定位策略 {i+1}: {locator}")
                
                # 检查元素是否存在
                if self.is_element_exist(locator):
                    print(f"  ✅ 找到复选框元素 (策略 {i+1})")
                    
                    # 获取元素信息用于调试
                    element = self.driver.find_element(*locator)
                    content_desc = element.get_attribute('content-desc')
                    text = element.get_attribute('text')
                    print(f"  📝 元素信息: content-desc='{content_desc}', text='{text}'")
                    
                    # 点击复选框
                    print(f"  👆 准备点击复选框...")
                    self.click_element(locator, f'登录_服务条款_策略{i+1}')
                    print(f"  ✅ 服务条款复选框点击成功 (策略 {i+1})")
                    
                    # 等待一下确保点击生效
                    time.sleep(1)
                    return True
                    
            except Exception as e:
                print(f"  ❌ 策略 {i+1} 失败: {e}")
                continue
        
        # 如果主要策略都失败，尝试查找所有包含相关文本的元素
        print("⚠️ 主要定位策略失败，尝试查找所有相关元素...")
        try:
            # 查找所有包含 "agree" 或 "policy" 的元素
            all_elements = self.driver.find_elements(AppiumBy.XPATH, "//*[contains(@content-desc, 'agree') or contains(@content-desc, 'policy') or contains(@content-desc, 'Agree') or contains(@content-desc, 'Policy')]")
            print(f"📋 找到 {len(all_elements)} 个相关元素")
            
            for j, elem in enumerate(all_elements):
                try:
                    content_desc = elem.get_attribute('content-desc')
                    text = elem.get_attribute('text')
                    print(f"    📝 元素 {j}: content-desc='{content_desc}', text='{text}'")
                    
                    # 如果元素包含相关文本，尝试点击
                    if content_desc and ('agree' in content_desc.lower() or 'policy' in content_desc.lower()):
                        print(f"    👆 准备点击元素 {j}...")
                        elem.click()
                        print(f"    ✅ 点击了元素 {j}: {content_desc}")
                        time.sleep(1)
                        return True
                        
                except Exception as e:
                    print(f"    ❌ 点击元素 {j} 失败: {e}")
                    continue
                    
        except Exception as e:
            print(f"❌ 查找相关元素失败: {e}")
        
        print("❌ 所有复选框定位策略都失败了")
        return False
       
    def save_mobile_login_state(self):
        """保存移动端登录状态"""
        try:
            import json
            import os
            from datetime import datetime
            
            # 创建登录状态数据
            login_state = {
                "timestamp": datetime.now().isoformat(),
                "platform": "Android",
                "app_package": "com.eiot6.solartest",
                "app_activity": "com.eiot6.solartest/.MainActivity",
                "device_name": "emulator-5554",
                "login_status": "success",
                "session_data": {
                    "device_id": self.get_device_id(),
                    "app_state": self.get_app_state(),
                    "current_activity": self.get_current_activity()
                }
            }
            
            # 保存到文件
            state_file = "mobile_login_state.json"
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(login_state, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 登录状态已保存到: {state_file}")
            print(f"📱 设备ID: {login_state['session_data']['device_id']}")
            print(f"📱 应用状态: {login_state['session_data']['app_state']}")
            print(f"📱 当前活动: {login_state['session_data']['current_activity']}")
            
        except Exception as e:
            print(f"❌ 保存登录状态失败: {e}")
    
    def get_device_id(self):
        """获取设备ID"""
        try:
            # 尝试获取设备ID
            device_id = self.driver.capabilities.get('deviceUDID', 'unknown')
            return device_id
        except:
            return "unknown"
    
    def get_app_state(self):
        """获取应用状态"""
        try:
            # 尝试获取应用状态
            app_state = self.driver.capabilities.get('appState', 'unknown')
            return app_state
        except:
            return "unknown"
    
    def get_current_activity(self):
        """获取当前活动"""
        try:
            # 尝试获取当前活动
            current_activity = self.driver.current_activity
            return current_activity
        except:
            return "unknown"
    
    def handle_permission_dialogs(self):
        """处理权限弹窗"""
        print("🔍 开始处理权限弹窗...")
        
        # 等待一下让弹窗出现
        time.sleep(2)
        
        # 定义可能的权限弹窗定位器
        permission_selectors = [
            # 方法1：通过文本定位
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("While using the app")'),
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("While using the app")'),
            # 方法2：通过XPath定位
            (AppiumBy.XPATH, "//*[@text='While using the app']"),
            (AppiumBy.XPATH, "//*[contains(@content-desc, 'While using the app')]"),
            # 方法3：通过按钮定位
            (AppiumBy.CLASS_NAME, "android.widget.Button"),
            # 方法4：通过可点击元素定位
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().clickable(true).text("While using the app")'),
        ]
        
        for i, selector in enumerate(permission_selectors):
            try:
                print(f"  🔍 尝试权限弹窗定位方法 {i+1}: {selector}")
                
                # 检查元素是否存在
                if self.is_element_exist(selector):
                    print(f"  ✅ 找到权限弹窗元素 (方法 {i+1})")
                    
                    # 获取元素信息用于调试
                    element = self.driver.find_element(*selector)
                    text = element.get_attribute('text')
                    content_desc = element.get_attribute('content-desc')
                    print(f"  📝 元素信息: text='{text}', content-desc='{content_desc}'")
                    
                    # 点击权限按钮
                    print(f"  👆 准备点击权限按钮...")
                    self.click_element(selector, f'登录_权限弹窗_方法{i+1}')
                    print(f"  ✅ 权限弹窗处理成功 (方法 {i+1})")
                    
                    # 等待一下确保点击生效
                    time.sleep(2)
                    
                    # 检查是否还有其他权限弹窗
                    self.handle_additional_permissions()
                    return True
                    
            except Exception as e:
                print(f"  ❌ 方法 {i+1} 失败: {e}")
                continue
        
        print("⚠️ 未找到权限弹窗，可能已经处理过了")
        return False
    
    def check_login_status(self):
        """检查登录状态"""
        try:
            import json
            import os
            
            state_file = "mobile_login_state.json"
            if not os.path.exists(state_file):
                print("❌ 未找到登录状态文件")
                return False
            
            with open(state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
            
            # 检查登录状态
            if state.get('login_status') == 'success':
                print("✅ 检测到已保存的登录状态")
                return True
            else:
                print("❌ 登录状态无效")
                return False
                
        except Exception as e:
            print(f"❌ 检查登录状态失败: {e}")
            return False
    
    def is_main_page(self):
        """检查是否在主页面"""
        try:
            # 等待页面加载
            time.sleep(2)
            
            # 检查是否有主页面特有的元素
            main_page_indicators = [
                # 检查是否有Plants元素（主页面底部导航）
                (AppiumBy.XPATH, "//android.view.View[contains(@content-desc, 'Plants')]"),
                # 检查是否有Device元素（主页面底部导航）
                (AppiumBy.XPATH, "//android.view.View[contains(@content-desc, 'Device')]"),
                # 检查是否有其他主页面元素
                (AppiumBy.XPATH, "//android.view.View[contains(@content-desc, 'Home')]"),
                (AppiumBy.XPATH, "//android.view.View[contains(@content-desc, 'Settings')]"),
            ]
            
            for indicator in main_page_indicators:
                if self.is_element_exist(indicator):
                    print(f"✅ 检测到主页面元素: {indicator[1]}")
                    return True
            
            print("❌ 未检测到主页面元素，可能还在登录页面")
            return False
            
        except Exception as e:
            print(f"❌ 检查主页面状态失败: {e}")
            return False

    # def get_error_info(self):
    #     """获取登录失败的提示信息"""
    #     return self.get_element_text(app_loc.error_info, '登录_失败提示信息')

    # def page_refresh(self):
    #     """刷新页面"""
    #     self.driver.get(url=self.url)