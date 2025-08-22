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
from common.handle_data import EnvData,get_standard_data

db = HandleMysql()


@pytest.fixture()
def antenna_edit_fixture(driver):
    """编辑更换监测器前添加新的监测器imei"""
    # 前置条件
    driver.implicitly_wait(5)
    #添加监测器
    detector_page = DetectorPage(driver)
    imei = 'sn'+str(int(time.time() * 1000))
    sn = 'sn'+str(int(time.time() * 1000))
    detector_page.click_to_add_delector()
    detector_page.detector_add(imei,sn,'1234')
    time.sleep(2)
   # setattr(EnvData,'detectonew',imei)
    sql = "select *from detector where imei = '{}'".format(imei)
    res = db.find_one(sql)
    res_id = res['id']
    res_imei = res['imei']
 #   setattr(EnvData, 'detectorId', id)
    yield (res_imei,res_id)
    AntenaPage(driver)

@allure.feature('天线')
@allure.description('天线编辑')
class TestAntenaEdit:
    """天线编辑-运营商
        天线编辑-监测器
        天线详情-基础参数配置
        天线详情-频段配置
        天线详情-监测器更换
        天线详情-重置监测频段
    """
    #编辑运营商的数据
    case_data = []
    case_data.append(eval(cases[6]['data']))

    #编辑更换监测器的数据
    case_data1 = []
    case_data1.append(eval(cases[7]['data']))


    @allure.story('天线编辑')
    @allure.title('正常编辑运营商')
    @pytest.mark.parametrize("case", case_data)
    def test_antena_edit_1_mnc(self, case,antenna_fixture,get_standard_data_fixture):
        #用例执行前获取标准数据
        pre_site, pre_antena, pre_antena_param,pre_antena_bands = get_standard_data_fixture

        antena_page = antenna_fixture
        # 进行编辑天线的操作（运营商）'0移动 1联通 2电信 3电联 4三网'
        case['mnc'] = 3
        case['number'] = getattr(EnvData,'antenna')
        case['detector'] = None
        antena_page.antena_edit_mnc_detector(case['number'],case['mnc'],case['detector'])

        # 校验天线编辑（通过查询数据库校验）
        time.sleep(3)
        sql = "select *from antenna where number = '{}'".format(case['number'])
        res = db.find_one(sql)
        res = res['mnc']

        #执行后获取标准数据
        site,antenna,antenna_param,antena_bands= get_standard_data()
        # 断言用例执行是否通过，标准数据未不改变
        try:
            assert case['mnc'] == res and site == pre_site and antenna == pre_antena and antenna_param == pre_antena_param
        except AssertionError as e:
            log.error("用例执行失败")
            log.exception(e)
            raise e
        else:
            log.info("用例执行通过")
          #  excel.write_data(7, 7, json.dumps(case))


    @allure.story('天线编辑')
    @allure.title('正常编辑更换检测器')
    @pytest.mark.parametrize("case", case_data1)
    def test_antena_edit_2_detector(self, case,antenna_fixture,antenna_edit_fixture,get_standard_data_fixture):
        pre_site, pre_antena, pre_antena_param,pre_antena_bands = get_standard_data_fixture
        antena_page = antenna_fixture
        # 进行编辑天线的操作-更换监测器
       # case['detector'], case['detectorId'] = antenna_edit_fixture
        case['number'] = getattr(EnvData,'antenna')
        case['detector'] = antenna_edit_fixture[0]
        case['detectorId'] = antenna_edit_fixture[1]
        case['mnc'] = None
        #case['number'] = getattr(EnvData, 'number')


        antena_page.antena_edit_mnc_detector(case['number'], case['mnc'], case['detector'])

        # 校验天线编辑（通过查询数据库校验）
        time.sleep(3)
        sql = "select *from antenna where number = '{}'".format(case['number'])
        res = db.find_one(sql)
        res = res['detector_id']

        site, antenna, antenna_param,antena_bands = get_standard_data()
        # 断言用例执行是否通过
        try:
            assert case['detectorId'] == res and site == pre_site and antenna == pre_antena and antenna_param == pre_antena_param
        except AssertionError as e:
            log.error("用例执行失败")
            log.exception(e)
            raise e
        else:
            log.info("用例执行通过")
           # excel.write_data(7, 7, json.dumps(case))


    @allure.story('天线详情')
    @allure.title('正常详情参数配置-基础配置')
    @pytest.mark.parametrize("case", case_data)
    def test_antena_info_3_param(self, case, antenna_fixture, get_standard_data_fixture):
        # 用例执行前获取标准数据
        pre_site, pre_antena, pre_antena_param ,pre_antena_bands= get_standard_data_fixture

        antena_page = antenna_fixture

        case['number'] = getattr(EnvData, 'antenna')
        case['learningCycle'] = 12

        antena_page.antena_edit_basicinfo(case['number'], case['learningCycle'])

        # 校验天线编辑（通过查询数据库校验）
        time.sleep(3)
        sql = "select *from antenna_param ap left join antenna a on ap.antenna_id=a.id where a.number = '{}'".format(case['number'])
        res = db.find_one(sql)
        res_learningCycle = res['learning_cycle']

        # 执行后获取标准数据
        site, antenna, antenna_param ,antena_bands= get_standard_data()
        # 断言用例执行是否通过，标准数据未不改变
        try:
            assert case['learningCycle'] == res_learningCycle and site == pre_site and antenna == pre_antena and antenna_param == pre_antena_param
        except AssertionError as e:
            log.error("用例执行失败")
            log.exception(e)
            raise e
        else:
            log.info("用例执行通过")

    @allure.story('天线详情')
    @allure.title('正常详情参数配置-频段设置')
    @pytest.mark.parametrize("case", case_data)
    def test_antena_info_4_band(self, case, antenna_fixture, get_standard_data_fixture):
        # 用例执行前获取标准数据
        pre_site, pre_antena, pre_antena_param,pre_antena_bands = get_standard_data_fixture

        antena_page = antenna_fixture

        case['number'] = getattr(EnvData, 'antenna')
        # case['mnc'] = getattr(EnvData, 'mnc')

       # case['number'] = 'an1703129796862'
        
        #执行前获取频段
        sql = "select *from antenna_param ap left join antenna a on ap.antenna_id=a.id where a.number = '{}'".format(case['number'])
        pre = db.find_one(sql)
        pre_first_band = list(eval(pre['daily_lte_bands']).values())[0][0]
        
        time.sleep(2)
        antena_page.antena_edit_bands(case['number'])
        time.sleep(2)
        
        # 执行后校验天线频段配置（通过查询数据库校验）'lte_bands': '{"4": ["1", "3", "8", "34", "39", "40", "41"]}'
        res = db.find_one(sql)
        res_band = list(eval(res['daily_lte_bands']).values())[0]

        # 执行后获取标准数据
        site, antenna, antenna_param,antena_bands = get_standard_data()
        # 断言用例执行是否通过，标准数据不改变
        try:
            assert pre_first_band not in res_band and site == pre_site and antenna == pre_antena and antenna_param == pre_antena_param
        except AssertionError as e:
            log.error("用例执行失败")
            log.exception(e)
            raise e
        else:
            log.info("用例执行通过")

    @allure.story('天线详情')
    @allure.title('正常详情更换监测器')
    @pytest.mark.parametrize("case", case_data)
    def test_antena_info_5_change(self, case, antenna_fixture, get_standard_data_fixture,antenna_edit_fixture):
        # 用例执行前获取标准数据
        pre_site, pre_antena, pre_antena_param,pre_antena_bans = get_standard_data_fixture
        antena_page = antenna_fixture
        # 进行编辑天线的操作-更换监测器
        # case['detector'], case['detectorId'] = antenna_edit_fixture
        case['number'] = getattr(EnvData, 'antenna')
        case['detector'] = antenna_edit_fixture[0]
        case['detectorId'] = antenna_edit_fixture[1]

        antena_page.antena_info_change_detector(case['number'], case['detector'])

        # 校验天线编辑（通过查询数据库校验）
        time.sleep(3)
        sql = "select *from antenna where number = '{}'".format(case['number'])
        res = db.find_one(sql)
        res = res['detector_id']

        site, antenna, antenna_param,antena_bands = get_standard_data()
        # 断言用例执行是否通过
        try:
            assert case['detectorId'] == res and site == pre_site and antenna == pre_antena and antenna_param == pre_antena_param
        except AssertionError as e:
            log.error("用例执行失败")
            log.exception(e)
            raise e
        else:
            log.info("用例执行通过")
        # excel.write_data(7, 7, json.dumps(case))




    @allure.story('天线详情')
    @allure.title('正常详情频段重置')
    @pytest.mark.parametrize("case", case_data)
    def test_antena_info_6_resetbands(self, case, antenna_fixture, get_standard_data_fixture):
        # 用例执行前获取标准数据
        pre_site, pre_antena, pre_antena_param,pre_antena_bands = get_standard_data_fixture

        antena_page = antenna_fixture

        case['number'] = getattr(EnvData, 'antenna')
        case['antenna_id'] = getattr(EnvData,'antenna_id')
    #     case['number'] = '1215'
    #     case['antenna_id'] = 840
        sql_insert = "insert into antenna_band(antenna_id,mnc,bands,freq,rsrp,cycle_status,`value`,reference_value,lac,bands_hz,bands_type) VALUES({},0,39,100,-50,1,'-32,-35,-34',-33,110,'1880-1920MHz',1)".format(case['antenna_id'])
        db.inser_one(sql_insert)
        time.sleep(2)
        
        antena_page.antena_edit_resetbands(case['number'])

        # 校验天线编辑（通过查询数据库校验）
        time.sleep(3)
        sql = "select *from antenna_band ap left join antenna a on ap.antenna_id=a.id where a.number = '{}'".format(case['number'])
        res = db.find_all(sql)

        # 执行后获取标准数据
        site, antenna, antenna_param,antena_bands = get_standard_data()

        # 断言用例执行是否通过，标准数据不改变
        try:
            assert res == () and site == pre_site and antenna == pre_antena and antenna_param == pre_antena_param and pre_antena_bands == antena_bands
        except AssertionError as e:
            log.error("用例执行失败")
            log.exception(e)
            raise e
        else:
            log.info("用例执行通过")
