from common.base_page import BasePage
from locator.locator_login import LoginLocator as loc
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from common.handle_config import conf
import time
import os

# 强制禁用代理
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['ALL_PROXY'] = ''
os.environ['all_proxy'] = ''

class LoginPage(BasePage):
    """登录页面"""
    # 登录的url地址
   # url = conf.get('env', 'base_url') + conf.get('url', 'login_url')

    url = 'https://solar-tst.eiot6.com/account/login'
    
    def setup_browser(self, keep_open=False):#True 保持浏览器打开，False 关闭浏览器
        options = Options()
        options.add_experimental_option('detach', keep_open)
        
        # 添加代理绕过选项
        options.add_argument('--no-proxy-server')
        options.add_argument('--proxy-bypass-list=*')
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        
        # 添加其他选项（去掉无头模式，这样可以看到浏览器窗口）
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        
        # 使用本地安装的ChromeDriver
        chrome_driver_path = "/opt/homebrew/bin/chromedriver"
        try:
            self.driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
        except Exception as e:
            print(f"Chrome启动失败，尝试备用路径: {e}")
            # 备用路径
            self.driver = webdriver.Chrome(service=Service('/Users/mayun/chromedriver'), options=options)
        
        self.driver.get(self.url)
        time.sleep(3)
        return self.driver

    def __init__(self, driver):
        """
        :param driver: webdriver对象
        :type driver: WebDriver
        """
        super().__init__(driver)
        # 使用传入的driver，不创建新的浏览器实例
        self.driver.implicitly_wait(15) 

    def login(self, user, pwd):
        """输入账号密码点击登录"""
        # 检查是否已经登录
        current_url = self.driver.current_url
        print(f"当前页面URL: {current_url}")
        
        if 'login' not in current_url:
            print("检测到可能已经登录，尝试检查登录状态...")
            try:
                from locator.locator_index import IndexLocator as index_loc
                self.wait_element_visibility(index_loc.index, '综合概览', timeout=5)
                print("✅ 已经登录，无需重新登录")
                return
            except:
                print("未检测到登录状态，继续登录流程...")
        
        # 确保在登录页面
        if 'login' not in self.driver.current_url:
            self.driver.get(self.url)
            time.sleep(2)
        
        self.input_text(loc.username_loc, user, '登录_账号输入')
        # 输入密码
        self.input_text(loc.pwd_loc, pwd, '登录_密码输入')
        # 服务条款
        self.click_element(loc.service_loc, '登录_服务条款')
        # 点击登录
        self.click_element(loc.login_loc, '登录_点击元素')
        
        # 等待页面加载
        time.sleep(5)
        
        # 尝试点击"我是服务商"按钮，使用多个定位器
        try:
            print("尝试点击'我是服务商'按钮...")
            self.click_element(loc.me_service, '登录_我是服务商')
        except Exception as e1:
            print(f"第一个定位器失败: {e1}")
            try:
                print("尝试备用定位器1...")
                self.click_element(loc.me_service_alt, '登录_我是服务商_备用1')
            except Exception as e2:
                print(f"备用定位器1失败: {e2}")
                try:
                    print("尝试备用定位器2...")
                    self.click_element(loc.me_service_alt2, '登录_我是服务商_备用2')
                except Exception as e3:
                    print(f"备用定位器2失败: {e3}")
                    try:
                        print("尝试备用定位器3...")
                        self.click_element(loc.me_service_alt3, '登录_我是服务商_备用3')
                    except Exception as e4:
                        print(f"所有定位器都失败，跳过点击'我是服务商'按钮")
                        print(f"错误信息: {e4}")
                        # 不抛出异常，继续执行
                        pass
        
        # 等待登录完成，检查是否成功跳转到主页面
        print("等待登录完成...")
        time.sleep(8)  # 增加等待时间
        
        # 检查是否成功登录（等待综合概览或光伏运营元素出现）
        try:
            from locator.locator_index import IndexLocator as index_loc
            self.wait_element_visibility(index_loc.index, '综合概览', timeout=15)
            print("✅ 登录成功，已跳转到主页面")
        except Exception as e:
            print(f"⚠️ 等待综合概览元素超时: {e}")
            # 不抛出异常，继续执行
            pass
    def get_error_info(self):
        """获取登录失败的提示信息"""
        return self.get_element_text(loc.error_info, '登录_失败提示信息')

    def page_refresh(self):
        """刷新页面"""
        self.driver.get(url=self.url)
