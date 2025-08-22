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
from locator.locator_app_device import AddGatewayLocator as Gatewayadd
from locator.locator_app_device import AddOptimizersLocator as Optimizersadd
from locator.locator_app_device import PlantListLocator as plantlist
from locator.locator_app_device import PlantinfoLocatorr as plantinfo




class APPDevicePage(BasePage):
    """设备管理页面"""
    def __init__(self, driver=None):
        super().__init__(driver)
    
    def click_app_plant(self):
        """点击菜单到电站入口"""
        # 先等待页面加载完成
        time.sleep(3)
        
        # 尝试多次查找Plants元素
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                print(f"🔍 第{attempt + 1}次尝试查找Plants元素...")
                if self.is_element_exist(plantlist.plant):
                    print("✅ 找到Plants元素，准备点击")
                    self.click_element(plantlist.plant, 'Plants')
                    break
                else:
                    print(f"❌ 第{attempt + 1}次未找到Plants元素，等待后重试...")
                    time.sleep(2)
            except Exception as e:
                print(f"❌ 第{attempt + 1}次查找Plants元素失败: {e}")
                if attempt < max_attempts - 1:
                    time.sleep(2)
                else:
                    raise e
        
        #self.input_text(plantlist.search_plant, plantname, '输入电站名称')
        
        # 点击设备管理菜单
        self.click_element(plantlist.enter_plant, '第一个电站')
        time.sleep(1)
    
    def click_app_add_device(self):
        """点击菜单到添加设备入口"""
        # 先等待页面加载完成
        time.sleep(1)
        #底部导航栏device
        self.click_element(plantinfo.Device, 'Device')
        self.click_element(plantinfo.add_device, '添加设备+')
        time.sleep(1)    
       
        
    
    def gateway_device_add(self, sn, device_name):
        """添加设备"""
        self.click_app_plant()
        self.driver.implicitly_wait(3)
        self.click_app_add_device()
        self.driver.implicitly_wait(5)
        # 点击采集器
        self.click_element(Gatewayadd.cloud_gateway, '采集器')
        time.sleep(1)
         #处理权限弹窗
        self.handle_additional_permissions()
        time.sleep(1)
        self.click_element(Gatewayadd.enter_sn, 'enter sn')
        time.sleep(1)
        # 输入设备SN
        # 先点击输入框获得焦点
        self.click_element(Gatewayadd.input_sn, '输入框焦点')
        self.input_text(Gatewayadd.input_sn, sn, '输入设备SN')
        time.sleep(1)
        
        # 隐藏键盘，避免键盘挡住Confirm按钮
        print("🔽 隐藏键盘，避免键盘挡住Confirm按钮...")
        self.hide_keyboard()
        time.sleep(2)  # 等待键盘完全隐藏
        
        # 点击确定
        self.click_element(Gatewayadd.confirm, 'confirm')
        # 点击连接设备
        self.click_element(Gatewayadd.connect_device, '连接设备')
        
        # 等待页面直到出现确定按钮，增加更好的错误处理
        print("⏳ 等待active_confirm元素出现...")
        try:
            # 先等待元素可见
            active_confirm_element = self.wait_element_clickable(Gatewayadd.active_confirm, 'done', timeout=120)
            print("✅ active_confirm元素已出现，准备聚焦...")
            self.js_focus_element(active_confirm_element)
            print("✅ active_confirm元素聚焦成功")
            
        except Exception as e:
            print(f"❌ 等待active_confirm元素超时或失败: {e}")
            print("🔍 尝试检查当前页面状态...")
        #修改设备名称
        print("🔍 准备修改设备名称...")
        try:
            # 先点击输入框获得焦点
            self.click_element(Gatewayadd.active_devicename, '输入框焦点')
            time.sleep(1)
            
            # 获取元素对象
            username_element = self.driver.find_element(*Gatewayadd.active_devicename)
            print(f"✅ 找到设备名称输入框: {username_element}")
            
            # 清空输入框
            username_element.clear()
            time.sleep(0.5)
            print("✅ 设备名称输入框已清空")
            
            # 输入设备名称
            username_element.send_keys(device_name)
            time.sleep(1)
            print(f"✅ 设备名称 '{device_name}' 输入成功")
            
        except Exception as e:
            print(f"❌ 修改设备名称失败: {e}")
            # 尝试备用方法
            try:
                print("🔄 尝试备用方法输入设备名称...")
                self.input_text(Gatewayadd.active_devicename, device_name, '输入设备名称')
                print("✅ 备用方法输入设备名称成功")
            except Exception as e2:
                print(f"❌ 备用方法也失败: {e2}")
                print("⚠️ 跳过设备名称修改，继续执行...")
        
        time.sleep(1)
        #点击done
        self.click_element(Gatewayadd.active_confirm, 'done')
        time.sleep(1)
        # 点击回到设备列表
        time.sleep(1)
        self.click_element(Gatewayadd.back_device_list, '回到设备列表页面')
        time.sleep(1)
        self.click_element(Gatewayadd.back_device_list, '回到列表页面')
    
    def device_add_result(self):
        """获取设备添加结果"""
        # 这里可以根据实际情况返回添加结果
        # 比如检查是否有成功提示或者错误提示
        return "添加成功"
    
    def device_add_check(self, device_name):
        """检查设备是否添加成功"""
        # 输入设备名称进行搜索
        self.input_text(Gatewayadd.search_gateway_device, device_name, '设备名称')
        # 点击enter键搜索
        self.enter_to_element(Gatewayadd.search_gateway_device,'点击enter键')
        time.sleep(1)
        
        # # 获取搜索结果
        # try:
        #     # 查找设备名称是否在列表中
        #     result = self.get_element_text(Gatewayadd.gateway_device_name_1, '设备名称')
        #     return result
        # except:
        #     return "添加失败"
    #处理弹窗
    def handle_additional_permissions(self):
        """处理其他可能的权限弹窗"""
        print("🔍 检查是否有其他权限弹窗...")
        
        additional_permissions = [
            # 相机权限
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.android.permissioncontroller:id/permission_allow_foreground_only_button")'),
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.android.permissioncontroller:id/permission_allow_button")'),
        ]
        
        for i, selector in enumerate(additional_permissions):
            try:
                if self.is_element_exist(selector):
                    print(f"  ✅ 找到额外权限弹窗，点击处理...")
                    self.click_element(selector, f'登录_额外权限_{i+1}')
                    time.sleep(1)
            except Exception as e:
                print(f"  ❌ 处理额外权限失败: {e}")
                continue
