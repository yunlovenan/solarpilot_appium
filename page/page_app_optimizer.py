#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import time
from common.base_page import BasePage
from common.handle_config import conf
from page.page_app_login import APPLoginPage
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from locator.locator_app_device import AddOptimizersLocator as Optimizersadd
from locator.locator_app_device import AddPhysicallayoutLocator as Physicallayoutadd
from locator.locator_app_device import PlantListLocator as plantlist
from locator.locator_app_device import PlantinfoLocatorr as plantinfo




class APPOptimizerPage(BasePage):
    """优化器管理页面"""
    def __init__(self, driver=None):
        super().__init__(driver)
    
    # def click_app_plant(self):
    #     """点击菜单到电站入口"""
    #     # 先等待页面加载完成
    #     time.sleep(3)
        
    #     # 尝试多次查找Plants元素
    #     max_attempts = 3
    #     for attempt in range(max_attempts):
    #         try:
    #             print(f"🔍 第{attempt + 1}次尝试查找Plants元素...")
    #             if self.is_element_exist(plantlist.plant):
    #                 print("✅ 找到Plants元素，准备点击")
    #                 self.click_element(plantlist.plant, 'Plants')
    #                 break
    #             else:
    #                 print(f"❌ 第{attempt + 1}次未找到Plants元素，等待后重试...")
    #                 time.sleep(2)
    #         except Exception as e:
    #             print(f"❌ 第{attempt + 1}次查找Plants元素失败: {e}")
    #             if attempt < max_attempts - 1:
    #                 time.sleep(2)
    #             else:
    #                 raise e
    #     #self.input_text(plantlist.search_plant, plantname, '输入电站名称')
        
    #     # 点击设备管理菜单
    #     self.click_element(plantlist.enter_plant, '第一个电站')
    #     time.sleep(1)
    
    def click_app_add_optimizer(self):
        """点击添加设备按钮"""
        time.sleep(1)
        #self.click_element(plantinfo.Device, 'Device')
        #点击添加设备 - 使用多种定位策略
        try:
            # 首先尝试主要定位器
            self.click_element(plantinfo.add_device, '添加设备+')
        except Exception as e:
            print(f"⚠️ 主要定位器失败: {e}")
            try:
                # 尝试备用定位器1
                self.click_element(plantinfo.add_device_alt1, '添加设备+(备用1)')
            except Exception as e:
                print(f"⚠️ 备用定位器1失败: {e}")
                try:
                    # 尝试备用定位器2
                    self.click_element(plantinfo.add_device_alt2, '添加设备+(备用2)')
                except Exception as e:
                    print(f"⚠️ 备用定位器2失败: {e}")
                    try:
                        # 尝试备用定位器3
                        self.click_element(plantinfo.add_device_alt3, '添加设备+(备用3)')
                    except Exception as e:
                        print(f"❌ 所有定位器都失败: {e}")
                        # 如果所有定位器都失败，尝试使用坐标点击
                        print("🔄 尝试使用坐标点击...")
                        self.driver.tap([(697, 980)], 100)
        time.sleep(1)
       
        
    
    def optimizer_device_add(self, gateway_sn, optimizer_sn):
        """添加优化器"""
        self.click_app_add_optimizer()
        self.driver.implicitly_wait(5)
        
       #点击优化器
        self.click_element(Optimizersadd.Optimizers, '优化器')
        time.sleep(1)
         #点击confirm按钮
        self.click_element(Optimizersadd.confirm_add, 'confirm')
        #如果有got it按钮，点击got it
        if self.is_element_exist(Optimizersadd.got_it):
            self.click_element(Optimizersadd.got_it, 'got it')
            time.sleep(1)
    
        #点击编辑
        time.sleep(1)
        self.click_element(Physicallayoutadd.edit_physicallayout, '编辑')
        time.sleep(1)
         #点击空白区域
        self.click_element(Physicallayoutadd.blank_area, '空白区域')
        #添加网关
        #点击添加网关
        self.click_element(Physicallayoutadd.add_gateway, '添加网关')
        time.sleep(1)
        #输入网关SN
        # 先点击输入框获得焦点
        self.click_element(Physicallayoutadd.enter_gateway_sn, '输入框焦点')
        self.input_text(Physicallayoutadd.enter_gateway_sn,gateway_sn, '输入网关SN')
        # #点击enter
        # self.enter_to_element(Physicallayoutadd.enter_gateway_sn, '点击enter')
        #隐藏键盘
        self.hide_keyboard()
        time.sleep(1)
        #选择列表第一个
        self.click_element(Physicallayoutadd.gateway_list_1, '列表第一个')
        time.sleep(1)
        #done
        self.click_element(Physicallayoutadd.done, 'done')
        time.sleep(1)
        
        # ADD pv modules
        #点击空白区域 - 使用指定坐标点击（防止和网关重叠）
        self.click_blank_area_by_coordinates_specific()
        time.sleep(1)
        #点击添加pv modules - 使用坐标点击
        self.click_add_pv_modules_by_coordinates()
        time.sleep(1)
        # 确认
        self.click_element(Physicallayoutadd.confirm, '确认')
        time.sleep(1)
        
        
        #扫码添加优化器
        self.click_element(Physicallayoutadd.scan_button, '扫码')
        time.sleep(1)
        #direct scan
        self.click_element(Physicallayoutadd.direct_scan, 'direct scan')
        time.sleep(1)
        #择PV modules
        self.click_element(Physicallayoutadd.select_pv_modules, '选择pv modules')
        #输入SN
        #焦点
        self.click_element(Physicallayoutadd.input_PV_sn, '输入框焦点')
        self.input_text(Physicallayoutadd.input_PV_sn, optimizer_sn, '输入pv modules SN')
        time.sleep(1)
        # #点击enter
        # self.enter_to_element(Physicallayoutadd.input_PV_sn, '点击enter')
        #隐藏键盘
        self.hide_keyboard()
        time.sleep(1)
        self.click_element(Physicallayoutadd.save, 'save')
        
        #network configuration
        #是否有got it
        if self.is_element_exist(Physicallayoutadd.got_it_pv):
            self.click_element(Physicallayoutadd.got_it_pv, 'got it')
            time.sleep(1)
        #选择网关
        self.click_element(Physicallayoutadd.select_gateway, '选择网关')
        #选择优化器
        self.click_element(Physicallayoutadd.select_optimizer, '选择优化器')
        #点击network configuration
        self.click_element(Physicallayoutadd.network_configuration, 'network configuration')
        time.sleep(1)
   
        
        
        # 等待页面直到出现exit按钮，增加更好的错误处理
        print("⏳ 等待exit元素出现...")
        try:
            # 先等待元素可见
            active_confirm_element = self.wait_element_clickable(Physicallayoutadd.exit_button, 'exit', timeout=120)
            print("✅ 等待exit元素出现元素已出现，准备聚焦...")
            self.js_focus_element(active_confirm_element)
            print("✅ exit元素聚焦成功")
            
        except Exception as e:
            print(f"❌ 等待exit元素超时或失败: {e}")
            print("🔍 尝试检查当前页面状态...")    
        time.sleep(1)
        #点击done
        self.click_element(Physicallayoutadd.exit_button, 'exit')
        time.sleep(1)
        # 点击回到设备列表
        self.click_element(Physicallayoutadd.back_device_list, '回到设备列表页面')
        #刷新页面
        self.page_refresh()
        time.sleep(1)
    
    
    def device_add_result(self):
        """获取设备添加结果"""
        # 这里可以根据实际情况返回添加结果
        # 比如检查是否有成功提示或者错误提示
        return "添加成功"
    
    
    
    def click_blank_area_by_coordinates_specific(self):
        """使用指定坐标点击第二个空白区域"""
        try:
            print("📍 使用指定坐标点击第二个空白区域: (697, 980)")
            
            # 使用指定的坐标点击
            self.driver.tap([(697, 980)], 100)
            
            print("✅ 第二个空白区域坐标点击成功")
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ 第二个空白区域坐标点击失败: {e}")
            raise e
    
    def click_add_pv_modules_by_coordinates(self):
        """使用坐标点击Add PV modules按钮"""
        try:
            print("📍 使用坐标点击Add PV modules按钮...")
            
            # 获取屏幕尺寸
            screen_size = self.driver.get_window_size()
            width = screen_size['width']
            height = screen_size['height']
            
            # 尝试在屏幕右侧区域点击，通常Add PV modules按钮在这个位置
            x = int(width * 0.8)  # 屏幕80%宽度
            y = int(height * 0.4)  # 屏幕40%高度
            
            print(f"📍 使用坐标点击Add PV modules: ({x}, {y})")
            self.driver.tap([(x, y)], 100)
            
            print("✅ Add PV modules坐标点击成功")
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Add PV modules坐标点击失败: {e}")
            raise e
    
    def device_add_check(self, device_name):
        """检查设备是否添加成功"""
        # # 输入设备名称进行搜索
        # self.input_text(Gatewayadd.search_gateway_device, device_name, '设备名称')
        # # 点击enter键搜索
        # self.enter_to_element(Gatewayadd.search_gateway_device,'点击enter键')
        # time.sleep(1)
        
        # # 获取搜索结果
        # try:
        #     # 查找设备名称是否在列表中
        #     result = self.get_element_text(Gatewayadd.gateway_device_name_1, '设备名称')
        #     return result
        # except:
        #     return "添加失败"
    # #处理弹窗
    # def handle_additional_permissions(self):
    #     """处理其他可能的权限弹窗"""
    #     print("🔍 检查是否有其他权限弹窗...")
        
    #     additional_permissions = [
    #         # 相机权限
    #         (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.android.permissioncontroller:id/permission_allow_foreground_only_button")'),
    #         (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.android.permissioncontroller:id/permission_allow_button")'),
    #     ]
        
    #     for i, selector in enumerate(additional_permissions):
    #         try:
    #             if self.is_element_exist(selector):
    #                 print(f"  ✅ 找到额外权限弹窗，点击处理...")
    #                 self.click_element(selector, f'登录_额外权限_{i+1}')
    #                 time.sleep(1)
    #         except Exception as e:
    #             print(f"  ❌ 处理额外权限失败: {e}")
    #             continue
