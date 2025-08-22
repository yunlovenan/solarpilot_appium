from common.base_page import BasePage
from locator.locator_antena import AntenaAddLocator as antenaadd
from locator.locator_antena import AntennalistLocator as antenalist
from locator.locator_antena import AntenaInfoLocator as antenainfo
import time
from selenium.webdriver.common.action_chains import ActionChains

class AntenaPage(BasePage):
    """天线
    1、添加天线
    2、编辑天线
    3、天线详情参数设置（基础配置、频段配置）
    4、天线监测器更换
    """

    def click_antenan_add(self):
        "点击菜单项到添加天线入口"
        self.click_element(antenalist.menu_moniter, '监测管理')
        self.click_element(antenalist.menu_antenna, '室分天线')
        self.wait_element_visibility(antenalist.antenna_add,'添加天线按钮可见')
        self.click_element(antenalist.antenna_add, '+添加天线')

    def click_antenan_detail(self,antena):
        
        self.click_element(antenalist.menu_moniter, '监测管理')
        self.click_element(antenalist.menu_antenna, '室分天线')
        time.sleep(2)
      #  self.driver.refresh()
        if(self.get_element_attribute(antenalist.antenna_search,'value','输入框有内容')):
            self.click_element(antenalist.antenna_search_clear,'删除已输入内容')
        self.input_text(antenalist.antenna_search, antena, '输入查询天线编号')
        self.enter_to_element(antenalist.antenna_search, '点击查询')
        time.sleep(3)
        self.click_element(antenalist.antenna_info, '详情')
        
    def antenan_add(self,siteId,mnc,antena_num,antena_position,antenna_detectorId,antenna_pic):
        "添加天线"
        self.click_antenan_add()
        time.sleep(2)
        self.input_text(antenaadd.siteId, siteId, '站点名称')
        time.sleep(2)
        self.arrow_down_enter_to_element()

        # self.click_element(antenaadd.mnc, '点击运营商')
        # self.arrow_down_enter_to_element()

        mnc_input = self.get_element(antenaadd.mnc,'获取运营商框')
        ActionChains(self.driver).click(mnc_input).perform()
        time.sleep(2)
        if mnc == 0:
            self.click_element(antenaadd.mnc_select_1, '选择移动')
        elif mnc == 1:
            self.click_element(antenaadd.mnc_select_2, '选择联通')
        elif mnc == 2:
            self.click_element(antenaadd.mnc_select_3, '选择电信')
        elif mnc == 3:
            self.click_element(antenaadd.mnc_select_4, '选择电联')
        else:
            self.click_element(antenaadd.mnc_select_5, '选择三网')
        time.sleep(2)

        self.input_text(antenaadd.antena_num,antena_num, '天线编号')

        self.input_text(antenaadd.antena_position, antena_position, '天线安装位置')

        time.sleep(2)
        self.input_text(antenaadd.antenna_detectorId,antenna_detectorId, '监测器')
        time.sleep(2)
        self.arrow_down_enter_to_element()
        time.sleep(3)
        self.input_pic(antenaadd.antenna_pic,antenna_pic,'上传图片')
        time.sleep(3)
        self.click_element(antenaadd.antenna_submit,'提交')


    def check_antenan_add(self,number):
        """通过搜索查询校验天线是否添加成功"""
        try:
            self.input_text(antenalist.antenna_search, number, '输入查询天线编号')
            self.enter_to_element(antenalist.antenna_search, '点击查询')
            time.sleep(3)
            text = self.get_element_text(antenalist.antenna, '获取天线编号')
        except:
            return '添加失败'
        else:
            return text


    def antena_edit_mnc_detector(self,antena,mnc,detector):
        """编辑天线---监测器
            1、点击天线列表-编辑
            2、修改运营商'0移动 1联通 2电信 3电联 4三网'
            3、提交
            """
        self.click_element(antenalist.menu_moniter, '监测管理')
        self.click_element(antenalist.menu_antenna, '室分天线')
        time.sleep(2)
        #搜素天线
       # self.driver.refresh()
       # self.get_element(antenalist.antenna_search,'清除天线编号输入框').clear()
        time.sleep(2)
        self.input_text(antenalist.antenna_search, antena, '输入查询天线编号')
        self.enter_to_element(antenalist.antenna_search, '点击查询')
        time.sleep(3)
        self.click_element(antenalist.antenna_edit, '编辑')
        time.sleep(3)
        if mnc :
            mnc_input = self.get_element(antenaadd.mnc, '获取运营商框')
            ActionChains(self.driver).click(mnc_input).perform()
            time.sleep(2)
            if mnc == 0:
                self.click_element(antenaadd.mnc_select_1, '选择移动')
            elif mnc == 1:
                self.click_element(antenaadd.mnc_select_2, '选择联通')
            elif mnc == 2:
                self.click_element(antenaadd.mnc_select_3, '选择电信')
            elif mnc == 3:
                self.click_element(antenaadd.mnc_select_4, '选择电联')
            else:
                self.click_element(antenaadd.mnc_select_5, '选择三网')
            time.sleep(2)

        if detector:
            self.input_text(antenaadd.antenna_detectorId, detector, '编辑监测器')
            time.sleep(2)
            self.arrow_down_enter_to_element()
            time.sleep(3)
        self.click_element(antenaadd.antenna_submit, '提交')


    def antena_edit_basicinfo(self,antena,learningCycle):
        """天线详情修改参数配置
            1、点击天线列表-详情
            2、修改参数配置-基础配置
            3、提交
            """
        self.click_antenan_detail(antena)
        time.sleep(2)
        self.click_element(antenainfo.antenna_param,'参数设置')
        time.sleep(2)
        self.learningCycle_removes = self.get_elements(antenainfo.remove,'获取删除按钮')
        self.learningCycle_removes[1].click()

        time.sleep(1)
        self.input_text(antenainfo.learningCycle,learningCycle,'修改自学习周期')
        self.click_element(antenainfo.submit,'提交')

        # self.click_element(antenainfo.bands_tab, '频段配置')
        # self.click_element(antenainfo.band_remove, '频段删除第一个')
        # self.click_element(antenainfo.submit, '提交')


    def antena_edit_bands(self,antena):
        """天线详情修改频段配置
            1、点击天线列表-详情
            2、修改参数配置-频段配置
            3、提交
            """
        self.click_antenan_detail(antena)
        # self.click_element(antenalist.menu_moniter, '监测管理')
        # self.click_element(antenalist.menu_antenna, '室分天线')
        # time.sleep(2)
        # self.driver.refresh()
        # self.input_text(antenalist.antenna_search, antena, '输入查询天线编号')
        # self.enter_to_element(antenalist.antenna_search, '点击查询')
        # time.sleep(3)
        # self.click_element(antenalist.antenna_info, '详情')
        
        self.click_element(antenainfo.antenna_param,'参数配置')
        time.sleep(2)
        self.click_element(antenainfo.bands_tab, '频段配置')
        # self.bandlist = self.get_elements(antenainfo.all_band_input,'频段输入框')
        # self.firdtband = self.bandlist[1]

        self.bandremovelist = self.get_elements(antenainfo.band_remove, '频段删除x')
        time.sleep(1)
        self.bandremovelist[0].click()
        time.sleep(1)
        self.click_element(antenainfo.submit,'提交')


    def antena_info_change_detector(self,antena,detector):
        """天线详情更换监测器
            1、点击天线列表-详情
            2、监测终端-更换
            3、提交
            """
        self.click_antenan_detail(antena)
        # self.click_element(antenalist.menu_moniter, '监测管理')
        # self.click_element(antenalist.menu_antenna, '室分天线')
        # 
        # self.driver.refresh()
        # time.sleep(2)
        # self.input_text(antenalist.antenna_search, antena, '输入查询天线编号')
        # self.enter_to_element(antenalist.antenna_search, '点击查询')
        # time.sleep(3)
        # self.click_element(antenalist.antenna_info, '详情')
        time.sleep(2)
        self.click_element(antenainfo.detector_tab,'监测终端')
        self.click_element(antenainfo.detector_change, '更换')
        time.sleep(2)
        self.input_text(antenainfo.detector_input, detector, '监测器')
        time.sleep(2)
        self.arrow_down_enter_to_element()
        time.sleep(2)
        self.click_element(antenainfo.detector_change_confirm, '确定')

    def antena_edit_resetbands(self,antena):
        """天线详情重置频段
            1、点击天线列表-详情
            2、频段信息-重置频段
            3、提交
            """
        self.click_antenan_detail(antena)
        # self.click_element(antenalist.menu_moniter, '监测管理')
        # self.click_element(antenalist.menu_antenna, '室分天线')
        # time.sleep(2)
        # self.driver.refresh()
        # self.input_text(antenalist.antenna_search, antena, '输入查询天线编号')
        # self.enter_to_element(antenalist.antenna_search, '点击查询')
        # time.sleep(3)
        # self.click_element(antenalist.antenna_info, '详情')
        self.click_element(antenainfo.bandinfo_tab,'频段信息')
        self.click_element(antenainfo.reset_bands, '重置频段')
        self.wait_element_visibility(antenainfo.con_reset_bands,'确定重置监测频段')
        self.click_element(antenainfo.con_reset_bands,'确定')

    def antena_delete(self, antena):
        """天线删除
        点击天线列表-删除
            """
        self.click_element(antenalist.menu_moniter, '监测管理')
        self.click_element(antenalist.menu_antenna, '室分天线')

       # self.driver.refresh()
        time.sleep(2)
        self.input_text(antenalist.antenna_search, antena, '输入查询天线编号')
        self.enter_to_element(antenalist.antenna_search, '点击查询')
        time.sleep(2)
      #  self.wait_element_visibility(antenalist.antenna_delete,'等待查询结果显示')
        self.click_element(antenalist.antenna_delete, '删除')
        time.sleep(2)
     #   self.wait_element_visibility(antenalist.antenna_delete_re, '等待弹窗删除确认框')
        self.click_element(antenalist.antenna_delete_re, '确定删除')