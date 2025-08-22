import pytest
from data.case_data import LoginCase
from common.handle_logging import log
from page.page_app_device import APPDevicePage
from selenium import webdriver
import allure
import os
from common.handle_path import DATA_DIR
from common.handle_excel import HandleExcel
from testcase.conftest import cases
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from page.page_app_login import APPLoginPage
from common.handle_config import conf


@pytest.fixture(scope='class')
def app_gateway_fixture(driver):
    """添加设备功能的前置后置"""
    # 前置条件
    log.info("开始执行添加设备的用例")
    
    # 使用缓存的登录状态
    app_login_page = APPLoginPage(driver)
    app_device_page = APPDevicePage(driver)
    
    # 检查是否有缓存的登录状态
    log.info("检查缓存的登录状态...")
    if app_login_page.check_login_status():
        log.info("✅ 使用缓存的登录状态")
        # 确保应用完全加载到主页面
        log.info("⏳ 等待应用完全加载...")
        time.sleep(5)  # 增加等待时间
        
        # 检查是否在主页面，如果不在则尝试完成登录流程
        log.info("🔍 检查应用是否在主页面...")
        if not app_login_page.is_main_page():
            log.info("⚠️ 应用不在主页面，尝试完成登录流程...")
            case = eval(cases[0]['data'])  # 读取excel中的登录数据
            app_login_page.APP_login(case['username'], case['password'])
            log.info("登录流程完成")
            time.sleep(5)
        else:
            log.info("✅ 应用已在主页面")
    else:
        log.info("❌ 未找到缓存的登录状态，需要先登录")
        # 执行登录操作
        case = eval(cases[0]['data'])  # 读取excel中的登录数据
        app_login_page.APP_login(case['username'], case['password'])
        log.info("登录流程完成")
        # 等待登录完成后的页面加载
        time.sleep(5)
    
    # 等待页面加载
    time.sleep(3)
    
    yield app_device_page

    # 后置条件
    time.sleep(2)
    log.info("添加设备的用例执行完毕")
    
    
@allure.feature('添加设备流程')
@allure.description('添加设备功能测试')
class TestAPPDevice:
    """测试添加设备"""
    
    # def setup_method(self):
    #     """设置测试数据"""
    #     #获取config.ini中的数据
    #     self.config = ConfigParser()
    #     self.config.read(os.path.join(DATA_DIR, 'config.ini'))
    #     self.device_data = self.config.get('device_data', 'zigbee_sn')
    #     self.device_data1 = self.config.get('device_data', 'wifi_sn')
    #     self.device_data2 = self.config.get('device_data', 'opt_sn_1')
    #     self.device_data3 = self.config.get('device_data', 'opt_sn_2')
    #     self.device_data4 = self.config.get('device_data', 'opt_sn_3')
        
    # 从配置文件中读取设备数据
    case_data = [{
        "zigbee_sn": conf.get("device_data", "zigbee_sn"),
        "device_name": conf.get("device_data", "device_name")
    }]
    @allure.story('添加网关设备')
    @allure.title('添加网关成功场景')
    @pytest.mark.parametrize("case",case_data)
    def test_gateway_device_add(self, case, app_gateway_fixture):
        #case = self.device_data
        app_gateway_device_page = app_gateway_fixture
        # 进行添加网关的操作
        app_gateway_device_page.gateway_device_add(case['zigbee_sn'],case['device_name'])
        # # 激活网关之后的信息
        # res = app_index_page.get_me_info()
        # 断言用例执行是否通过
        # try:
        #     res = app_gateway_device_page.get_gateway_device_name()
        #     if res:
        #          log.info("用例执行通过")
        # except AssertionError as e:
        #     log.error("用例执行失败")
        #     log.exception(e)
        #     raise e
        # else:
        #     log.info("用例执行通过")
            # 退出登录，重新访问登录页面
         #   index_page.click_quit()
            # 重新进入登录页面
          #  login_page.page_refresh()
    @pytest.mark.skip
    @allure.story('错误用户名密码登录')
    @allure.title('登录失败场景')
    @pytest.mark.parametrize('case', LoginCase.error_case_data)
    def app_test_login_error_case(self, case, app_login_fixture):
        """异常用例，窗口上有提示"""
        app_login_page, app_index_page = app_login_fixture
        # 刷新页面
        app_login_page.page_refresh()
        # 执行登录操作
        app_login_page.APP_login(case['username'], case['password'])
        # 获取实际提示结果
        result = app_login_page.get_error_info()
        # 断言
        try:
            assert case['expected'] == result
        except AssertionError as e:
            log.error("用例执行失败")
            log.exception(e)
            raise e
        else:
            log.info("用例执行通过")
