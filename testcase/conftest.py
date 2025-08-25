
from selenium import webdriver
from selenium.webdriver import Chrome

import pytest
import requests

from common.handle_config import conf
from common.handle_logging import log
from page.page_index import IndexPage
from page.page_login import LoginPage
from page.page_antena import AntenaPage
from page.page_site import SitePage
from common.handle_excel import HandleExcel
from common.handle_path import DATA_DIR
from common.handle_data import get_standard_data
#from common.handle_sql import HandleMysql
import os
import time

excel = HandleExcel(os.path.join(DATA_DIR, "cases.xlsx"), "main_stream")
cases = excel.read_data()


class EnvData:
    pass


@pytest.fixture(scope='class')
def antenna_fixture(driver):
    """天线的前置后置"""
    # 前置条件
    log.info("天线的用例执行开始")
    # driver = Chrome()
    driver.implicitly_wait(10)
    # 创建登录页面
    # login_page = LoginPage(driver)
    # # # 登录
    # login_page.login(user=conf.get('test_data', 'username'), pwd=conf.get('test_data', 'pwd'))
    # 创建天线管理对象
    antenna_page = AntenaPage(driver)
    yield antenna_page
    # 后置条件
    time.sleep(2)
  #  driver.quit()
    log.info("天线的用例执行完毕")

@pytest.fixture(scope='class')
def site_fixture(driver):
    """添加站点的前置后置"""
    # 前置条件
    log.info("站点的用例执行开始")
#    driver = Chrome(options=browser())
    #driver.implicitly_wait(30)
    # # 创建登录页面
    # login_page = LoginPage(driver)
    # # # 登录
    # login_page.login(user=conf.get('test_data', 'username'), pwd=conf.get('test_data', 'pwd'))
    # 创建站点管理对象
    site_page = SitePage(driver)
    
    yield site_page
    # 后置条件
 #   driver.quit()
    log.info("站点的用例执行完毕")



@pytest.fixture()
def get_standard_data_fixture():
    """获取标准数据"""
    # 前置条件
    log.info("开始获取标准数据")
    pre_site,pre_antena,pre_antena_param,pre_antena_bands = get_standard_data()
    yield pre_site,pre_antena,pre_antena_param,pre_antena_bands
    log.info("结束获取标准数据")
    




# def browser():
#     if conf.getboolean('env', "headless"):
#         """设置浏览启动的选项：无头模式"""
#         opt = webdriver.ChromeOptions()
#     #    opt.add_argument("--headless")
#         return opt
#     else:
#         return None



#设置为session，全部用例执行一次
@pytest.fixture(scope='session')
def driver():
    # 检查是否是移动端测试
    import sys
    import os
    # 更精确的移动端测试检测
    is_mobile_test = False
    
    # 检查命令行参数
    for arg in sys.argv:
        if 'test_app_01_login.py' in arg or 'app' in arg.lower():
            is_mobile_test = True
            break
    
    # 检查环境变量（可选）
    if os.environ.get('TEST_TYPE') == 'mobile':
        is_mobile_test = True
    
    # 检查当前运行的测试文件
    if 'test_app_01_login.py' in str(sys.argv):
        is_mobile_test = True
    
    # 检查环境变量强制指定测试类型
    if os.environ.get('FORCE_TEST_TYPE') == 'mobile':
        is_mobile_test = True
    elif os.environ.get('FORCE_TEST_TYPE') == 'web':
        is_mobile_test = False
    
    print(f"检测到的测试类型: {'移动端' if is_mobile_test else 'Web端'}")
    print(f"命令行参数: {sys.argv}")
    print(f"环境变量 TEST_TYPE: {os.environ.get('TEST_TYPE')}")
    print(f"环境变量 FORCE_TEST_TYPE: {os.environ.get('FORCE_TEST_TYPE')}")
    
    if is_mobile_test:
        # 移动端测试 - 使用Appium driver
        print('------------open mobile app------------')
        try:
            # 自动启动 Appium 服务器
            import subprocess
            import time
            import requests
            
            def start_appium_server():
                """启动 Appium 服务器"""
                try:
                    # 检查 Appium 是否已经在运行
                    try:
                        response = requests.get('http://localhost:4723/wd/hub/status', timeout=2)
                        if response.status_code == 200:
                            print("✅ Appium 服务器已在运行")
                            return True
                    except:
                        pass
                    
                    print("🚀 正在启动 Appium 服务器...")
                    # 启动 Appium 服务器
                    appium_process = subprocess.Popen([
                        'appium', 
                        '--base-path', '/wd/hub', 
                        '--allow-cors', 
                        '--log', 'appium.log', 
                        '--log-level', 'debug'
                    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    
                    # 等待服务器启动
                    max_wait = 30  # 最大等待30秒
                    for i in range(max_wait):
                        try:
                            response = requests.get('http://localhost:4723/wd/hub/status', timeout=2)
                            if response.status_code == 200:
                                print(f"✅ Appium 服务器启动成功 (耗时: {i+1}秒)")
                                return True
                        except:
                            pass
                        time.sleep(1)
                        if i % 5 == 0:
                            print(f"⏳ 等待 Appium 服务器启动... ({i+1}/{max_wait}秒)")
                    
                    print("❌ Appium 服务器启动超时")
                    return False
                    
                except Exception as e:
                    print(f"❌ 启动 Appium 服务器失败: {e}")
                    return False
            
            # 启动 Appium 服务器
            if not start_appium_server():
                raise Exception("无法启动 Appium 服务器")
            
            # 添加本地appium模块路径
            import os
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'appium_local'))
            
            from appium import webdriver
            from appium.options.android import UiAutomator2Options
            
            # 创建options
            options = UiAutomator2Options()
            options.platform_name = "Android"
            options.automation_name = "uiautomator2"
            options.device_name = "emulator-5554"
            options.app_package = "com.eiot6.solartest"
            options.app_activity = "com.eiot6.solartest.MainActivity"
            options.no_reset = True  # 保持应用状态，使用缓存的登录状态
            
            mobile_driver = webdriver.Remote('http://localhost:4723/wd/hub', options=options)
            print("✅ 移动端驱动初始化成功")
            print("📱 应用将保持登录状态，使用缓存的cookies登录")
            
        except Exception as e:
            print(f"❌ 移动端驱动初始化失败: {e}")
            raise e
        
        yield mobile_driver
        
        # 清理资源
        try:
            print("🔄 正在关闭移动端驱动...")
            mobile_driver.quit()
            print("✅ 移动端驱动已关闭")
        except Exception as e:
            print(f"⚠️ 关闭移动端驱动时出现异常: {e}")
        finally:
            # 更温和的清理方式，避免强制停止导致Inspector无法使用
            try:
                import subprocess
                print("🔄 正在优雅地清理UiAutomator2进程...")
                
                # 检查UiAutomator2进程是否还在运行
                result = subprocess.run("adb shell pgrep -f io.appium.uiautomator2.server", shell=True, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print("⚠️ 检测到UiAutomator2进程仍在运行，将保持运行以支持Inspector")
                    print("💡 如需完全清理，请手动执行: adb shell am force-stop io.appium.uiautomator2.server")
                else:
                    print("✅ UiAutomator2进程已正常退出")
                    
            except Exception as e:
                print(f"⚠️ 检查UiAutomator2进程时出现异常: {e}")
    
    else:
        # Web测试 - 使用Chrome driver
            global driver
            print('------------open browser------------')
            from selenium import webdriver
            chromeOptions = webdriver.ChromeOptions()
            # 设定下载文件的保存目录，
            # 如果该目录不存在，将会自动创建
            prefs = {"download.default_directory": "E:\\testDownload"}
            # 将自定义设置添加到Chrome配置对象实例中
            chromeOptions.add_experimental_option("prefs", prefs)
            chromeOptions.add_argument("--ignore-certificate-errors")
            # chromeOptions.add_argument('--disable-gpu')
            chromeOptions.add_argument('--unlimited-storage')
            # 添加代理绕过选项
            chromeOptions.add_argument('--no-proxy-server')
            chromeOptions.add_argument('--proxy-bypass-list=*')
            chromeOptions.add_argument('--disable-web-security')
            chromeOptions.add_argument('--allow-running-insecure-content')
            # 移除无头模式，让浏览器窗口可见
            # chromeOptions.add_argument('--headless')
            chromeOptions.add_argument('--disable-gpu')
            chromeOptions.add_argument('--no-sandbox')
            chromeOptions.add_argument('--disable-dev-shm-usage')
            
            # 使用本地安装的ChromeDriver
            chrome_driver_path = "/opt/homebrew/bin/chromedriver"
            try:
                driver = webdriver.Chrome(service=webdriver.chrome.service.Service(chrome_driver_path), options=chromeOptions)
                driver.maximize_window()
                # chrome由于每次都打开设置页面，暂时没有找到关闭的方法，需要切换操作窗口(火狐浏览器不需要切换窗口)
                windows = driver.window_handles  # 获取所有窗口
                driver.switch_to.window(windows[-1])  # 切换到最新窗口
            except Exception as e:
                print(f"浏览器启动失败: {e}")
                # 如果Chrome启动失败，尝试使用无头模式
                chromeOptions.add_argument('--headless')
                driver = webdriver.Chrome(service=webdriver.chrome.service.Service(chrome_driver_path), options=chromeOptions)

            # 自动加载 cookies 绕过登录
            try:
                import json
                cookies_file = "../solar_cookies.json"
                if os.path.exists(cookies_file):
                    print("发现 cookies 文件，正在加载...")
                    
                    # 先访问主域名，确保cookies能正确设置
                    driver.get("https://solar-tst.eiot6.com")
                    time.sleep(3)
                    
                    with open(cookies_file, 'r', encoding='utf-8') as f:
                        cookies = json.load(f)
                    
                    print(f"加载 {len(cookies)} 个cookies...")
                    for i, cookie in enumerate(cookies):
                        try:
                            # 确保cookie的domain正确
                            if 'domain' in cookie and cookie['domain'] == '.eiot6.com':
                                cookie['domain'] = '.solar-tst.eiot6.com'
                            driver.add_cookie(cookie)
                            print(f"✅ 成功添加cookie {i+1}: {cookie.get('name', 'unknown')}")
                        except Exception as e:
                            print(f"❌ 添加cookie {i+1} 失败: {e}")
                    
                    # 刷新页面并等待
                    print("刷新页面...")
                    driver.refresh()
                    time.sleep(5)
                    
                    # 检查是否成功登录
                    current_url = driver.current_url
                    print(f"当前页面URL: {current_url}")
                    
                    if 'login' not in current_url:
                        print("✅ Cookies 加载完成，已绕过登录")
                    else:
                        print("⚠️ Cookies 可能无效，需要手动登录")
                else:
                    print("未找到 cookies 文件，需要手动登录")
            except Exception as e:
                print(f"加载 cookies 时出错: {e}")
            
            yield driver
            print('------------测试完成，保持浏览器打开------------')
            # 调试模式下不关闭浏览器，让用户可以看到结果
            # driver.quit()


