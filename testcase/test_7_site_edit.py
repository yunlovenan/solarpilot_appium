import pytest

from common.handle_logging import log
from page.page_login import LoginPage
from page.page_detector import DetectorPage
from page.page_antena import AntenaPage
from selenium import webdriver
import allure
import time
import json
from testcase.conftest import cases, excel
from common.handle_sql import HandleMysql
from common.handle_config import conf
from common.handle_data import EnvData, get_standard_data

db = HandleMysql()

@allure.feature('电站编辑')
@allure.description('电站编辑')
class TestSiteEdit:
    """电站编辑-电站名称
        站点详情-基础参数配置
        站点详情-频段配置
        站点详情-重置监测频段
    """
    # 电站名称（新）
    #case_data = [{"sitename":"测试站点"}]
    # 电站名称（旧）
    site_data = []
    site_data.append(eval(cases[1]['real_data']))

   # @pytest.mark.skip
    @allure.story('电站编辑')
    @allure.title('正常编辑')
    @pytest.mark.parametrize("case", site_data)
    def test_site_edit(self, case, site_fixture, get_standard_data_fixture):
        # 用例执行前获取标准数据
        pre_site= get_standard_data_fixture

        site_page = site_fixture
        
        oldsitename =case['name']
        case['sitename'] = "st"+str(int(time.time() * 1000))

        site_page.site_edit(oldsitename,case['sitename'])

        # 校验电站名称编辑（通过查询数据库校验）
        time.sleep(3)
        sql = "SELECT * FROM eam_project WHERE project_name= '{}'".format(case['sitename'])
        res = db.find_one(sql)
        res = res['project_name']

        # 执行后获取标准数据
        site = get_standard_data()
        # 断言用例执行是否通过，标准数据未不改变
        try:
            assert case['sitename'] == res and site == pre_site
        except AssertionError as e:
            log.error("用例执行失败")
            log.exception(e)
            raise e
        else:
            log.info("用例执行通过")
            setattr(EnvData,'sitename',case['name'])



    # @allure.story('站点详情')
    # @allure.title('正常详情参数配置-基础配置')
    # @pytest.mark.parametrize("case", case_data)
    # def test_site_info_2_param(self, case, site_fixture, get_standard_data_fixture):
    #     # 用例执行前获取标准数据
    #     pre_site, pre_antena, pre_antena_param,pre_antena_bands = get_standard_data_fixture

    #     site_page = site_fixture

    #     case['sitename'] = getattr(EnvData, 'sitename')
    #     case['siteId'] = getattr(EnvData, 'siteId')
    #     # case['sitename'] = '测试站点'
    #     # case['siteId'] = 13
    #     case['learningCycle'] = 3

    #     site_page.site_change_param(case['sitename'], case['learningCycle'])

    #     #查看站点下天线的参数
    #     time.sleep(3)
    #     sql_site = "select  *from antenna_param  where site_id = {} and antenna_id is null ".format(case['siteId'])
    #     res_site = db.find_one(sql_site)
    #     sql = "select a.number,ap.learning_cycle from antenna_param ap left join antenna a on ap.antenna_id=a.id where ap.site_id = {} and a.deleted = 0".format(case['siteId'])
    #     res_antenna = db.find_all(sql)

    #     # 执行后获取标准数据
    #     site, antenna, antenna_param ,antena_bands= get_standard_data()
    #     # 断言用例执行是否通过，标准数据未不改变
    #     try:
    #         for antenna_para in res_antenna:

    #             assert case['learningCycle'] == antenna_para['learning_cycle'] 
    #         assert case['learningCycle'] == res_site['learning_cycle'] and site == pre_site and antenna == pre_antena and antenna_param == pre_antena_param
            
    #     except AssertionError as e:
    #         log.error("用例执行失败")
    #         log.exception(e)
    #         raise e
    #     else:
    #         log.info("用例执行通过")

    # @allure.story('站点详情')
    # @allure.title('站点详情参数配置-频段设置')
    # @pytest.mark.parametrize("case", case_data)
    # def test_site_info_3_band(self, case, site_fixture, get_standard_data_fixture):
    #     # 用例执行前获取标准数据
    #     pre_site, pre_antena, pre_antena_param,pre_antena_bands = get_standard_data_fixture

    #     site_page = site_fixture

    #     case['sitename'] = getattr(EnvData, 'sitename')
    #     case['siteId'] = getattr(EnvData, 'siteId')
    #     # case['sitename'] = '测试站点'
    #     # case['siteId'] = 13

    #     # 执行前获取频段
    #     sql = "select *from antenna_param  where site_id = {} and antenna_id is null".format(case['siteId'])
    #     pre = db.find_one(sql)
    #     pre_first_band = list(eval(pre['daily_lte_bands']).values())[0][0]

    #     time.sleep(2)
    #     site_page.site_change_bands(case['sitename'])
    #     time.sleep(2)

    #     # 执行后校验站点频段配置（通过查询数据库校验）'
    #     res = db.find_one(sql)
    #     res_band = list(eval(res['daily_lte_bands']).values())[0]

    #     # 执行后校验站点下天线频段配置---这得根据运营商去匹配，暂未做
    #    # sql = "select a.number,ap.learning_cycle from antenna_param ap left join antenna a on ap.antenna_id=a.id where ap.site_id = {} and a.deleted = 0".format(case['siteId'])
    #     #res_antenna = db.find_all(sql)

    #     # 执行后获取标准数据
    #     site, antenna, antenna_param,antena_bands= get_standard_data()
    #     # 断言用例执行是否通过，标准数据不改变
    #     try:

    #         assert pre_first_band not in res_band and site == pre_site and antenna == pre_antena and antenna_param == pre_antena_param
    #     except AssertionError as e:
    #         log.error("用例执行失败")
    #         log.exception(e)
    #         raise e
    #     else:
    #         log.info("用例执行通过")



    # @allure.story('站点详情')
    # @allure.title('站点详情频段重置')
    # @pytest.mark.parametrize("case", case_data)
    # def test_site_info_4_resetbands(self, case, site_fixture, get_standard_data_fixture):
    #     # 用例执行前获取标准数据
    #     pre_site, pre_antena, pre_antena_param, pre_antena_bands = get_standard_data_fixture

    #     site_page = site_fixture

    #     case['sitename'] = getattr(EnvData, 'sitename')
    #     case['siteId'] = getattr(EnvData, 'siteId')
    #     case['antenna_id'] = getattr(EnvData, 'antenna_id')
    #     # case['sitename'] = '测试站点'
    #     # case['siteId'] = 13
    #     # case['antenna_id'] = 852

    #     #先插入band
    #     sql_insert = "insert into antenna_band(antenna_id,mnc,bands,freq,rsrp,cycle_status,`value`,reference_value,lac,bands_hz,bands_type) VALUES({},0,39,100,-50,1,'-32,-35,-34',-33,110,'1880-1920MHz',1)".format(
    #         case['antenna_id'])
    #     db.inser_one(sql_insert)
    #     time.sleep(2)

    #     site_page.site_reset_band(case['sitename'])

    #     # 校验天线编辑（通过查询数据库校验）
    #     time.sleep(2)
    #     sql = "SELECT *from antenna_band ab LEFT JOIN antenna a on ab.antenna_id = a.id LEFT JOIN site s on a.site_id = s.id where s.id = {}".format(case['siteId'])
    #     res = db.find_all(sql)

    #     # 执行后获取标准数据
    #     site, antenna, antenna_param,antena_bands = get_standard_data()

    #     # 断言用例执行是否通过，标准数据不改变
    #     try:
    #         assert res == () and site == pre_site and antenna == pre_antena and antenna_param == pre_antena_param
    #     except AssertionError as e:
    #         log.error("用例执行失败")
    #         log.exception(e)
    #         raise e
    #     else:
    #         log.info("用例执行通过")
