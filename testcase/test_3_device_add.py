import pytest
from data.case_data import SiteCase
from common.handle_logging import log
from page.page_login import LoginPage
from page.page_index import IndexPage
from page.page_device import DevicePage
from selenium import webdriver
import allure
import time
import json
from testcase.conftest import cases,excel
from common.handle_sql import HandleMysql
from selenium.webdriver import Chrome
from common.handle_config import conf
from common.handle_data import EnvData

db = HandleMysql()
@pytest.fixture(scope='class')
def device_fixture(driver):
    """添加设备的前置后置"""
    # 前置条件
    log.info("设备的用例执行开始")
    driver.implicitly_wait(10)
    
    # # 检查登录状态，如果未登录则进行登录
    # current_url = driver.current_url
    # print(f"当前页面URL: {current_url}")
    
    # # 更智能的登录检测
    # if '/account/login' in current_url:
    #     print("检测到登录页面，进行登录...")
    #     login_page = LoginPage(driver)
    #     login_page.login(user=conf.get('test_data', 'username'), pwd=conf.get('test_data', 'pwd'))
    #     time.sleep(3)  # 等待登录完成
    # else:
    #     print("已登录状态，继续执行...")
    #     # 如果不在登录页面，尝试导航到主页面
    #     try:
    #         driver.get("https://solar-tst.eiot6.com")
    #         time.sleep(3)
    #     except Exception as e:
    #         print(f"导航到主页面失败: {e}")
    
    # 创建设备管理对象
    device_page = DevicePage(driver)
    # # 点击菜单到添加设备入口
    # device_page.click_to_add_device()

    yield device_page
    # 后置条件
    log.info("设备的用例执行完毕")
@allure.feature('设备')
@allure.description('设备添加')
class TestDetector:
    """测试设备"""
    device_case_data = [{"zigbee_sn":"GW1123C21122"}]
    
    @allure.story('设备添加')
    @allure.title('正常添加')
    @pytest.mark.parametrize("case", device_case_data)
    def test_site_add_pass(self, case, device_fixture):
        device_page = device_fixture
        # 进行添加监测器的操作（sn、imei唯一）
        case['gateway_name'] = 'gateway_'+str(int(time.time() * 1000))
        device_page.device_add(case['zigbee_sn'], case['gateway_name'])
        
        # #校验设备激活结果
        # result = device_page.device_add_result()
        
        # 校验设备添加(通过页面列表查询校验)
        res = device_fixture.device_add_check(case['gateway_name'])
        print(res)
        
      

   

        # #校验站点添加（通过查询数据库校验）
        # time.sleep(3)
        # sql = "select *from detector where imei = '{}'".format(case['imei'])
        # res = db.find_one(sql)

        # 断言用例执行是否通过
        try:
            assert case['gateway_name'] in res
        except AssertionError as e:
            log.error("用例执行失败")
            log.exception(e)
            raise e
        else:
            log.info("用例执行通过")
            excel.write_data(5,7,json.dumps(case))
            setattr(EnvData,"device_sn",case['zigbee_sn'])
            setattr(EnvData,"device_name",case['gateway_name'])
            #setattr(EnvData, "detectorId", res['id'])


