from common.base_page import BasePage
from locator.locator_antena import AntenaAddLocator as antenaadd
from locator.locator_antena import AntennalistLocator as antenalist
from locator.locator_antena import AntenaInfoLocator as antenainfo
import time


class AntenaInfoPage(BasePage):
    """天线详情
    1、点击天线详情
    2、点击参数配置
    3、修改参数配置
    4、提交

    """

    def click_antenan_info(self):
        "点击菜单项到天线详情入口"
        self.click_element(antenalist.menu_moniter, '监测管理')
        self.click_element(antenalist.menu_antenna, '室分天线')
        self.wait_element_visibility(antenalist.antenna_add, '添加天线按钮可见')
        self.click_element(antenalist.antenna_add, '+添加天线')

    def antenan_info_edit(self, siteId, antena_num, antena_position, antenna_detectorId, antenna_pic):
        "添加站点"
        self.wait_element_visibility(antenaadd.siteId, '进入添加页面')

        self.input_text(antenaadd.siteId, siteId, '站点名称')
        # self.wait_element_clickable(antenaadd.siteId_0, '站点选择列表可见')
        time.sleep(2)
        self.arrow_down_enter_to_element()

        self.click_element(antenaadd.mnc, '点击运营商')
        # self.wait_element_visibility(antenaadd.mnc_0,'运营商列表可见')
        # self.click_element(antenaadd.mnc_0,'选择运营商')
        self.arrow_down_enter_to_element()

        self.input_text(antenaadd.antena_num, antena_num, '天线编号')

        self.input_text(antenaadd.antena_position, antena_position, '天线安装位置')

        time.sleep(2)
        self.input_text(antenaadd.antenna_detectorId, antenna_detectorId, '监测器')
        time.sleep(2)
        self.arrow_down_enter_to_element()
        time.sleep(3)
        self.input_pic(antenaadd.antenna_pic, antenna_pic, '上传图片')
        time.sleep(3)
        self.click_element(antenaadd.antenna_submit, '提交')

    def check_antenan_add(self, number):
        try:
            self.input_text(antenalist.antenna_search, number, '输入查询天线编号')
            self.enter_to_element(antenalist.antenna_search, '点击查询')
            time.sleep(3)
            text = self.get_element_text(antenalist.antenna, '获取天线编号')
        except:
            return '添加失败'
        else:
            return text