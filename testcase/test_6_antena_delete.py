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




@pytest.fixture(scope='class')
def detector_add_fixture(driver):
    """添加监测器"""
    # 前置条件
    driver.implicitly_wait(5)
    #添加监测器
    detector_page = DetectorPage(driver)
    imei = 'sn'+str(int(time.time() * 1000))
    sn = 'sn'+str(int(time.time() * 1000))
    detector_page.click_to_add_delector()
    detector_page.detector_add(imei,sn,'1234')
    time.sleep(2)
    sql = "select *from detector where imei = '{}'".format(imei)
    res = db.find_one(sql)
    res_id = res['id']
    res_imei = res['imei']
    yield res_imei,res_id
    # 后置条件
    time.sleep(1)
    #  driver.quit()
    log.info("天线的用例执行完毕")


@pytest.fixture(scope='class')
def antenna_add_fixture(driver,antenna_fixture,detector_add_fixture):
    """添加天线"""
    # 前置条件
    driver.implicitly_wait(5)

    antena_page = antenna_fixture
    sitename = getattr(EnvData, 'sitename')
   # sitename = 'ST1702880021714'
    mnc = '联通'
    number = 'an' + str(int(time.time() * 1000))
    position = '利尔达'
    detectorId = detector_add_fixture[0]
    installPic = r"D:\Python311\code\antenna\antenna\data\123.jpg"

    antena_page.click_antenan_add()
    antena_page.antenan_add(sitename, mnc, number, position, detectorId,installPic)

    time.sleep(2)
    sql = "select *from antenna where number = '{}'".format(number)
    res = db.find_one(sql)
    res_number = res['number']
    yield res_number
    # 后置条件
    time.sleep(1)
  #  driver.quit()
   # log.info("天线的用例执行完毕")

@allure.feature('天线')
@allure.description('天线删除')
class TestAntenaDetelte:
    """测试天线删除"""
    case_data = [{"number":"delete"}]
    @allure.story('天线删除')
    @allure.title('正常删除')
    @pytest.mark.parametrize("case", case_data)
    def test_antena_delete(self, case,antenna_fixture,antenna_add_fixture,get_standard_data_fixture):

        antena_page = antenna_fixture
        pre_site, pre_antena, pre_antena_param,pre_antena_bands = get_standard_data_fixture

        case['number'] = antenna_add_fixture

        antena_page.antena_delete(case['number'])

        # 校验天线编辑（通过查询数据库校验）
        time.sleep(2)
        sql = "select *from antenna where number = '{}'".format(case['number'])
        res = db.find_one(sql)
        res_deleted = res['deleted']
        res_detector_id = res['detector_id']
        site, antenna, antenna_param,antena_bands = get_standard_data()
        # 断言用例执行是否通过
        try:
            assert res_deleted ==0 and res_detector_id == None and site == pre_site and antenna == pre_antena and antenna_param == pre_antena_param
        except AssertionError as e:
            log.error("用例执行失败")
            log.exception(e)
            raise e
        else:
            log.info("用例执行通过")
