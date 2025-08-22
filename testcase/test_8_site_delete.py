import pytest

from common.handle_logging import log
from page.page_login import LoginPage
from page.page_detector import DetectorPage
from page.page_site import SitePage
from selenium import webdriver
import allure
import time
import json
from testcase.conftest import cases, excel
from common.handle_sql import HandleMysql
from common.handle_config import conf
from common.handle_data import EnvData,get_standard_data

db = HandleMysql()




# @pytest.fixture(scope='class')
# def site_add_fixture(driver):
#     """添加监测器"""
#     # 前置条件
#     driver.implicitly_wait(5)

#     site_page = SitePage(driver)

#     name = 'ST' + str(int(time.time() * 1000))
#     number = 'ST' + str(int(time.time() * 1000))
#     addrCode = 'ST' + str(int(time.time() * 1000))
#     contact = '123'
#     phone = '15356127976'
#     address = '利尔达'
#     site_page.site_add(name, number, addrCode, contact, phone, address)
#     time.sleep(2)
#     sql = "select *from site where name = '{}'".format(name)
#     res = db.find_one(sql)
#     res_name = res['name']
#     print(res_name)
#     yield res_name

    # # 后置条件
    # time.sleep(1)
    # #  driver.quit()
    # log.info("用例执行完毕")



@allure.feature('站点')
@allure.description('站点删除')
class TestSiteDelete:
    """测试监测器删除"""
    case_data = []
    case_data.append(eval(cases[1]['real_data']))
    @allure.story('电站删除')
    @allure.title('电站下无设备删除')
    @pytest.mark.parametrize("case", case_data)
    def test_site_delete_1(self, case,site_fixture,get_standard_data_fixture):

        site_page = site_fixture
        pre_site = get_standard_data_fixture

        site_page.site_delete(case['name'])

        # 校验站点已删除
        time.sleep(2)
        sql = "SELECT * FROM eam_project WHERE project_name= '{}' and is_delete=0".format(case['name'])
        res = db.find_one(sql)
        
        # 处理数据库查询结果
        if res is None:
            log.info("站点已删除或不存在")
            res_deleted = 1  # 假设删除成功
        else:
            res_deleted = res['is_delete']
        
        site = get_standard_data()
        # 断言用例执行是否通过
        try:
            assert res_deleted != 0 and site == pre_site
        except AssertionError as e:
            log.error("用例执行失败")
            log.exception(e)
            raise e
        else:
            log.info("用例执行通过")

    # @allure.story('站点删除')
    # @allure.title('站点下有天线，站点不能删除')
    # @pytest.mark.parametrize("case", case_data)
    # def test_site_delete_2(self, case, site_fixture,site_add_fixture, get_standard_data_fixture):
    #
    #     site_page = site_fixture
    #     pre_site, pre_antena, pre_antena_param, pre_antena_bands = get_standard_data_fixture
    #
    #     case['name'] = site_add_fixture
    #     print(case['name'])
    #
    #     site_page.site_delete(case['name'])
    #
    #     # 校验站点是否删除
    #     time.sleep(2)
    #     sql = "select *from site where name = '{}'".format(case['name'])
    #     res = db.find_one(sql)
    #     res_deleted = res['deleted']
    #
    #     site, antenna, antenna_param, antena_bands = get_standard_data()
    #     # 断言用例执行是否通过
    #     try:
    #         assert res_deleted == 1 and site == pre_site and antenna == pre_antena and antenna_param == pre_antena_param
    #     except AssertionError as e:
    #         log.error("用例执行失败")
    #         log.exception(e)
    #         raise e
    #     else:
    #         log.info("用例执行通过")