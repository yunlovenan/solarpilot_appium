import pytest
from data.case_data import LoginCase
from common.handle_logging import log
from page.page_app_login import APPLoginPage
from page.page_app_index import APPIndexPage
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

@pytest.fixture(scope='class')
def app_login_fixture(driver):
    """APP登录功能的前置后置"""
    # 前置条件
    log.info("开始执行APP登录的用例")
     # 前置条件
    app_login_page = APPLoginPage(driver)
    app_index_page = APPIndexPage(driver)
    yield app_login_page, app_index_page

    # 后置条件
    time.sleep(2)
    log.info("登录的用例执行完毕")
    
    
@allure.feature('登录流程')
@allure.description('登录界面功能测试')
class TestAppLogin:
    """测试登录"""
    
    def setup_method(self):
        """设置测试数据"""
        self.login_case_data = []
        self.login_case_data.append(eval(cases[0]['data'])) #读取excel中的数据
    @allure.story('正确用户名密码登录')
    @allure.title('登录成功场景')
    def test_login_pass(self, app_login_fixture):
        case = eval(cases[0]['data'])
        print(case)
        app_login_page, app_index_page = app_login_fixture
        # 进行登录的操作
        app_login_page.APP_login(case['username'], case['password'])
        # 获取登录之后的用户信息
        res = app_index_page.get_me_info()
        # 断言用例执行是否通过
        try:
            assert '登录成功' == res
        except AssertionError as e:
            log.error("用例执行失败")
            log.exception(e)
            raise e
        else:
            log.info("用例执行通过")
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
