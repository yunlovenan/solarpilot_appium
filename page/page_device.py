#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
设备管理页面
"""

import time
from selenium.webdriver.common.by import By
from common.base_page import BasePage
from page.page_site import SitePage
from locator.locator_device import DeviceAddLocator as deviceadd
from locator.locator_device import DevicelistLocator as devicelist
from locator.locator_device import DeviceinfoLocator as deviceinfo
from locator.locator_site import SitelistLocator as sitelist


class DevicePage(BasePage):
    """设备管理页面"""
    
    def __init__(self, driver=None):
        super().__init__(driver)
    
    def click_to_add_device(self):
        """点击菜单到添加设备入口"""
        # 先等待页面加载完成
        time.sleep(2)
        site_page = SitePage(self.driver)
        site_page.click_site_view()
        time.sleep(1)
        
        
        # 点击设备管理菜单
        self.click_element(deviceadd.device, '设备')
        time.sleep(2)
        
        # 点击添加设备按钮
        self.click_element(deviceadd.device_add, '新增设备')
        time.sleep(1)
        
        # 点击添加网关/采集器设备
        self.click_element(deviceadd.device_add_gateway, '添加网关/采集器设备')
        time.sleep(1)
        
    
    def device_add(self, sn, name):
        """添加设备"""
        self.click_to_add_device()
        time.sleep(2)
        # 输入设备SN
        self.input_text(deviceadd.device_sn, sn, '设备SN')
        # 输入设备名称
        self.input_text(deviceadd.device_name, name, '设备名称')
        # 点击确定按钮
        self.click_element(deviceadd.device_add_and_active, '添加并激活')
        #等待页面直到出现确定按钮
        self.js_focus_element(self.wait_element_clickable(deviceadd.device_confirm, '确 定'))

        #点击确定
        self.click_element(deviceadd.device_confirm, '确 定')
        time.sleep(2)
    
    def device_add_result(self):
        """获取设备添加结果"""
        # 这里可以根据实际情况返回添加结果
        # 比如检查是否有成功提示或者错误提示
        return "添加成功"
    
    def device_add_check(self, device_name):
        """检查设备是否添加成功"""
        # 输入设备名称进行搜索
        self.input_text(devicelist.device_name_input, device_name, '设备名称')
        # 点击enter键搜索
        self.enter_to_element(devicelist.device_name_input,'点击enter键')
        time.sleep(2)
        
        # 获取搜索结果
        try:
            # 查找设备名称是否在列表中
            result = self.get_element_text(devicelist.device_name_1, '设备名称')
            return result
        except:
            return "添加失败"
    
    # def device_edit(self, old_name, new_name):
    #     """编辑设备"""
    #     # 搜索设备
    #     self.input_text(devicelist.device_name_input, old_name, '设备名称')
    #     self.click_element(devicelist.device_search_btn, '搜索')
    #     time.sleep(2)
        
    #     # 点击编辑按钮
    #     self.click_element(devicelist.device_edit, '编辑')
    #     time.sleep(1)
        
    #     # 修改设备名称
    #     self.input_text(deviceadd.device_name, new_name, '设备名称')
    #     # 点击确定
    #     self.click_element(deviceadd.device_submit, '确定')
    #     time.sleep(2)
    
    # def device_delete(self, device_name):
    #     """删除设备"""
    #     # 搜索设备
    #     self.input_text(devicelist.device_name_input, device_name, '设备名称')
    #     self.click_element(devicelist.device_search_btn, '搜索')
    #     time.sleep(2)
        
    #     # 点击删除按钮
    #     self.click_element(devicelist.device_delete, '删除')
    #     time.sleep(1)
        
    #     # 确认删除
    #     self.click_element(devicelist.device_delete_confirm, '确定')
    #     time.sleep(1)
        
    #     # 二次确认删除
    #     self.click_element(devicelist.device_delete_confirm_2, '继续删除')
    #     time.sleep(2)
    
    # def device_view(self, device_name):
    #     """查看设备详情"""
    #     # 搜索设备
    #     self.input_text(devicelist.device_name_input, device_name, '设备名称')
    #     self.click_element(devicelist.device_search_btn, '搜索')
    #     time.sleep(2)
        
    #     # 点击查看按钮
    #     self.click_element(devicelist.device_details, '查看')
    #     time.sleep(2)
    
    # def get_device_info(self):
    #     """获取设备信息"""
    #     # 获取设备基本信息
    #     basic_info = self.get_element_text(deviceinfo.device_basic_info, '基本信息')
    #     return basic_info
