import pytest
from data.case_data import SiteCase
from common.handle_logging import log
from page.page_login import LoginPage
from page.page_index import IndexPage
from page.page_site import SitePage
from selenium import webdriver
import allure
import time
import json
from testcase.conftest import cases,excel
from common.handle_sql import HandleMysql
from common.handle_data import EnvData

db = HandleMysql()


@allure.feature('电站')
@allure.description('电站添加')
class TestSite:
    """测试添加站点"""
    site_case_data = []
    site_case_data.append(eval(cases[1]['data']))
    @allure.story('站点添加')
    @allure.title('正常添加')
    @pytest.mark.parametrize("case", site_case_data)
    def test_site_add_pass(self, case, site_fixture):
        site_page = site_fixture
        # 进行添加站点的操作（站点、编号、编址唯一）
        case['name'] = 'ST'+str(int(time.time() * 1000))
        # case['number'] = 'ST'+str(int(time.time() * 1000))
        # case['addrCode'] = 'ST' + str(int(time.time() * 1000))
        site_page.site_add(case['name'], case['capacity'],case['address'],case['contact'],case['phone'],case['price'])

        #校验站点添加(通过页面列表查询校验)
        #res = site_page.site_add_check(case['name'])
        #print(res)
        
         #查询电站
        res_query = site_page.site_add_check(case['name'])
        print(res_query)

        #校验查询结果
        try:
            assert res_query == case['name']
        except AssertionError as e:
            log.error("查询站点失败")
            log.exception(e)
            raise e
        #校验站点添加（通过查询数据库校验）
        time.sleep(2)
        sql = "SELECT * FROM eam_project WHERE project_name= '{}'".format(case['name'])
        res = db.find_one(sql)
        # 断言用例执行是否通过
        try:
            assert case['name'] == res['project_name'] #数据库名称project_name 断言站点名称是否一致
        except AssertionError as e:
            log.error("用例执行失败")
            log.exception(e)
            raise e
        else:
            log.info("用例执行通过")
            excel.write_data(3,7,json.dumps(case))
            setattr(EnvData,'sitename',case['name'])
            #setattr(EnvData, 'siteId', res['id'])
            