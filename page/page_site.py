from common.base_page import BasePage
from locator.locator_index import IndexLocator as loc
from locator.locator_site import SiteAddLocator as siteadd
from locator.locator_site import SitelistLocator as sitelist
from locator.locator_site import SiteinfoLocator as siteinfo
import pytest
from data.case_data import SiteCase
from selenium.webdriver.common.keys import Keys

import time

class SitePage(BasePage):
    """
    1、添加电站
    2、编辑电站
    3、电站详情
    4、添加

    """
    #新增电站入口
    def click_site_add(self):
        "点击菜单项到添加站点入口"
        self.click_element(sitelist.site, '电站列表')
        #self.click_element(sitelist.site_info, '站点信息管理')
        self.click_element(sitelist.site_add, '新增电站')
    #查看电站入口
    def click_site_view(self):
        "点击菜单项到查看站点入口"
        self.click_element(sitelist.site, '电站列表')
        #self.click_element(sitelist.site_info, '站点信息管理')
        #电站列表的第一条数据-查看
        time.sleep(1)
        self.click_element(sitelist.site_details, '查看')

    #关于电站入口
    def click_site_edit(self):
        "点击菜单项到编辑站点入口"
        self.click_site_view()
        time.sleep(1)
        self.click_element(sitelist.site_about, '关于电站')
    #删除电站入口
    def click_site_delete(self):
        "点击菜单项到删除站点入口"
        self.click_site_view()
        time.sleep(5)
        self.click_element(sitelist.site_delete, '删除')


    def site_add(self,sitename,capacity,address,contact,phone,price):
        "添加站点"
        # 点击菜单到添加站点入口
        self.click_site_add()
        
        # 先清除电站名称内容，再输入新名称
        element = self.get_element(siteadd.site_name,'电站名称')
        element.click()  # 先点击获得焦点
        element.clear()   # 清空内容
        time.sleep(0.5)  # 短暂等待确保清空完成
        self.input_text(siteadd.site_name, sitename, '电站名称')

        self.click_element(siteadd.site_type, '电站类型')
        time.sleep(1)
        #self.arrow_down_enter_to_element()
        self.enter_to_element(siteadd.site_type,'点击enter键')
    
        
        self.click_element(siteadd.site_system,'系统类型')
        time.sleep(1)
        #self.arrow_down_enter_to_element()
        self.enter_to_element(siteadd.site_system,'点击enter键')
    
        self.input_text(siteadd.site_capacity, capacity, '装机功率')
        
        
        self.click_element(siteadd.site_country, '国家/地区')
        time.sleep(1)
        #self.arrow_down_enter_to_element()
        self.enter_to_element(siteadd.site_country,'点击enter键')
        
        self.click_element(siteadd.site_map,'经纬度')
        time.sleep(2)
        
        self.input_text(siteadd.site_address, address, '电站地址')
        time.sleep(1) 
         
        self.click_element(siteadd.site_address_select, '选择地址')
      
        
        self.driver.implicitly_wait(5)
        self.click_element(siteadd.site_confirm, '确定')
        
        #self.input_text(siteadd.site_timezone, timezone, '电站时区')
        #self.js_focus_element(self.wait_element_clickable(siteadd.timezone_select,'东八区'))

        self.input_text(siteadd.contact, contact, '联系人')

        self.input_text(siteadd.phone, phone, '手机号')
        self.driver.implicitly_wait(5)
        self.click_element(siteadd.site_next, '下一步')
        #电价配置
        self.driver.implicitly_wait(2)
        self.input_text(siteadd.site_price, price, '电价')
        time.sleep(1)
        self.click_element(siteadd.site_next, '下一步')
        time.sleep(2)
        self.click_element(siteadd.site_complete, '完成')

    #     self.click_element(siteadd.site_area, '选择站点区域')
        
    #     self.js_focus_element(self.wait_element_clickable(siteadd.province_select,'选择省'))

    #     self.js_focus_element(self.wait_element_clickable(siteadd.city_select, '选择市'))

    #     self.js_focus_element(self.wait_element_clickable(siteadd.district_select, '选择区'))

    #     self.driver.implicitly_wait(5)
    #   #  self.input_text(siteadd.site_address,siteaddress,'站点地址')
    #     #self.driver.implicitly_wait(3)
    #     #self.arrow_down_enter_to_element()

    #     self.click_element(siteadd.site_amap,'点击地图上地址')

    #     time.sleep(3)
    #     self.click_element(siteadd.submitbutton, '提交')





    def site_add_check(self,sitename):
        self.driver.implicitly_wait(3)
        try:
            self.input_text(sitelist.site_search,sitename,'搜索框站点名称输入查询')
            self.enter_to_element(sitelist.site_search,'点击查询')
            time.sleep(5)
            text = self.get_element_text(sitelist.sitename_1,'获取站点名称')
        except:
            return '添加失败'
        else:
            return text

    def site_edit(self,oldsitename,newsitename):
        "编辑电站名称"
        self.driver.implicitly_wait(3)
        self.click_site_edit()
        time.sleep(3)
        self.input_text(sitelist.site_search, oldsitename, '输入查询站点名称')
        self.enter_to_element(sitelist.site_search, '点击查询')
        time.sleep(2)
        # 先清除电站名称内容，再输入新名称
        element = self.get_element(siteadd.site_name,'电站名称')
        element.click()
        time.sleep(2)
        element.send_keys(Keys.COMMAND + "a")  # 全选，windows系统使用ctrl+a，mac系统使用command+a
        element.send_keys(Keys.DELETE) 
        time.sleep(0.5)  # 短暂等待确保清空完成
        self.input_text(siteadd.site_name, newsitename, '站点名称')
        self.click_element(sitelist.site_edit, '更新基本信息')
        time.sleep(2)


    def site_to_detail(self,sitename):
        "进入详情"
        self.click_element(sitelist.site, '站点管理')
        self.click_element(sitelist.site_info, '站点信息管理')
        time.sleep(2)
        #  self.driver.refresh()
        if self.get_element_attribute(sitelist.site_search,'value','站点输入框有内容'):
            self.click_element(sitelist.site_search_clear,'删除输入框内容')
        self.input_text(sitelist.site_search, sitename, '输入查询站点名称')
        self.enter_to_element(sitelist.site_search, '点击查询')
        time.sleep(2)
        self.click_element(sitelist.site_details, '详情')
        time.sleep(2)


    def site_change_param(self,sitename,learningCycle):
        "站点详情-参数配置-基础参数设置"
        self.site_to_detail(sitename)

        self.click_element(siteinfo.site_param_tab, '参数设置')
        time.sleep(2)
        self.learningCycle_removes = self.get_elements(siteinfo.site_param_remove, '获取删除按钮')
        self.learningCycle_removes[1].click()

        time.sleep(1)
        self.input_text(siteinfo.site_learningCycle, learningCycle, '修改自学习周期')
        self.click_element(siteinfo.site_submit, '提交')

    def site_change_bands(self,sitename):
        "详情-参数配置-频段配置"
        self.site_to_detail(sitename)
        self.click_element(siteinfo.site_param_tab, '参数设置')
        time.sleep(1)
        self.click_element(siteinfo.site_bands, '频段配置')
        time.sleep(1)
        self.bandremovelist = self.get_elements(siteinfo.band_remove, '频段删除x')
        time.sleep(1)
        self.bandremovelist[0].click()
        time.sleep(1)
        self.click_element(siteinfo.site_submit, '提交')
        
    def site_reset_band(self,sitename):
        "详情-参数配置-重置频段"
        self.site_to_detail(sitename)
        self.click_element(siteinfo.site_reset_bands,'重置频段')
        self.wait_element_visibility(siteinfo.site_reset_bands_confirm,'等待弹窗确认')
        self.click_element(siteinfo.site_reset_bands_confirm,'确认重置频段')
        

    def site_delete(self,name):
        # self.click_element(sitelist.site, '站点管理')
        # self.click_element(sitelist.site_info, '站点信息管理')

        # # self.driver.refresh()
        # time.sleep(2)
        # self.input_text(sitelist.site_search, name, '输入查询站点名称')
        # self.enter_to_element(sitelist.site_search, '点击查询')
        # time.sleep(2)
        # #  self.wait_element_visibility(antenalist.antenna_delete,'等待查询结果显示')
        # self.click_element(sitelist.site_delete, '删除')
        self.driver.implicitly_wait(3)
        self.click_site_delete()
        time.sleep(4)
        self.click_element(sitelist.site_delete_confirm, '确定删除')
        time.sleep(1)
        self.click_element(sitelist.site_delete_confirm_2, '继续删除')
        time.sleep(1)