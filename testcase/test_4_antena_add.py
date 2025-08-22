import pytest

from common.handle_logging import log
from page.page_login import LoginPage

from page.page_antena import AntenaPage
from selenium import webdriver
import allure
import time
import json
from testcase.conftest import cases,excel
from common.handle_sql import HandleMysql
from common.handle_config import conf
from common.handle_data import EnvData,BandData


db = HandleMysql()



@allure.feature('天线')
@allure.description('天线添加')
class TestAntena:
    """测试添加天线"""
    case_data = []
    case_data.append(eval(cases[3]['data']))
    @allure.story('天线添加')
    @allure.title('正常添加')
    @pytest.mark.parametrize("case", case_data)
    def test_antena_add_pass(self, case, antenna_fixture):
        antena_page = antenna_fixture
        # 进行添加天线的操作（number）
        #siteId, mnc, antena_num, antena_position, antenna_detectorId, antenna_pic C:\Users\lenovo\Downloads\123.png
        case['sitename']  = getattr(EnvData,'sitename')
        case['detector'] = getattr(EnvData,'detector')
        # case['sitename']  = 'ST1703064185439'
        # case['siteId'] = 140
        # case['detector'] = "sn1702886449391"
        # case['detectorId'] = 1064
        case['number'] = 'an'+str(int(time.time() * 1000))
        case['installPic'] = r"D:\Python311\code\antenna\antenna\data\123.jpg"
        case['mnc'] = 1

        antena_page.antenan_add(case['sitename'],case['mnc'],case['number'],case['position'],case['detector'],case['installPic'])

        #校验天线添加(通过页面列表查询校验)
        #res = antena_page.check_antenan_add(case['number'])
       # print(res)

        #校验天线添加（通过查询数据库校验）
        time.sleep(3)
        sql = "select *from antenna where number = '{}'".format(case['number'])
        res = db.find_one(sql)

        # sql_param =  "select *from antenna_param ap left join antenna an on an.id=ap.antenna_id  where an.number = {}".format(case['number'])
        # res2 = db.find_one(sql_param)
        
        # 断言用例执行是否通过
        try:
            assert case['number'] == res['number'] and getattr(EnvData,'siteId') == res['site_id'] and getattr(EnvData,'detectorId') == res['detector_id']
           # assert case['number'] == res['number'] and 140 == res['site_id'] and 1064 == res['detector_id']

        except AssertionError as e:
            log.error("用例执行失败")
            log.exception(e)
            raise e
        else:
            log.info("用例执行通过")
            excel.write_data(5,7,json.dumps(case))
            setattr(EnvData, "antenna", res['number'])
            setattr(EnvData, "antenna_id", res['id'])

            



