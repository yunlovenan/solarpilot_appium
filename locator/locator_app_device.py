from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

    #
   
    


class AddGatewayLocator:
    """添加站点页面的元素定位"""
    #采集器 cloud gateway
    cloud_gateway = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Cloud Connect Advanced")')
    #设备SN
    enter_sn = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Enter SN")')
    #设备SN输入框
    input_sn = (AppiumBy.CLASS_NAME, "android.widget.EditText")
    
    #确认
    confirm = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Confirm")')
    
    #连接设备按钮
    connect_device = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Connect to the device")')
    
    #激活信息
    active_devicename = (AppiumBy.CLASS_NAME, "android.widget.EditText")
    
    active_confirm = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Done")')
    
    #回到设备列表（点击两次）
    back_device_list = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(6)')
    
    #查询设备输入框
    search_gateway_device = (AppiumBy.CLASS_NAME, "android.widget.EditText")
    #列表第一条数据的设备名称
    gateway_device_name_1 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.TextView").instance(0)')
    #相机权限
    camera_permission = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.android.permissioncontroller:id/permission_allow_foreground_only_button")')
    camera_allow = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.android.permissioncontroller:id/permission_allow_button")')
    #通用按钮
    general_button = (AppiumBy.CLASS_NAME, "android.widget.Button")
    
class AddOptimizersLocator:
    """添加优化器页面的元素定位"""  
    #添加优化器入口
    Optimizers = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Optimizers")')
    #确认添加 - 使用多种定位策略
    confirm_add = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Confirm")')
    # 备用定位器
    confirm_add_alt1 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Confirm")')
    confirm_add_alt2 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.Button").description("Confirm")')
    confirm_add_alt3 = (AppiumBy.XPATH, "//android.widget.Button[contains(@content-desc, 'Confirm')]")
    confirm_add_alt4 = (AppiumBy.CLASS_NAME, "android.widget.Button")
    #got it
    got_it = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Got It")')
    

class AddPhysicallayoutLocator:
    """添加物理布局页面的元素定位"""
    #编辑物理视图入口
    edit_physicallayout = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(13)')
    #图纸按钮
    physicallayout_paper = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(12)')
    #跳过按钮
    skip_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Skip")')
    #下一步
    next_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Next")')
    
    #空白区域
    blank_area = (AppiumBy.CLASS_NAME, "android.widget.ImageView")
    
    
    #添加网关
    add_gateway = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Add Gateway")')
    #网关sn
    enter_gateway_sn = (AppiumBy.XPATH, '//android.widget.EditText')
    #网关列表第一个
    gateway_list_1 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(9)')
    #done按钮
    done = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Done")')
  
    
    
    #ADD PV modules
    #空白区域 - 修改为更精确的定位，避免点击左上角
    blank_area_2 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(6)')
   
    
     #添加pv modules - 尝试多种定位策略
    add_pv_modules = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Add PV modules")')
    
    #行数
    row_number = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("1").instance(0)')
    #列数
    column_number = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("1").instance(1)')
    #确认按钮
    confirm = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Confirm")')
    
    
    
    #扫码按钮
    scan_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(7)')
    #Direct Scan
    direct_scan = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Direct Scan")')
    #选择PV modules
    select_pv_modules = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(12)')
    #输入SN
    input_PV_sn = (AppiumBy.XPATH, '//android.widget.EditText')
    #索引
    index_PV = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(14)')
    #确认按钮
    confirm_PV = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Confirm")')
    
    #1:1还是1：2
    one_to_one = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(6)')
   
    #保存
    save = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(8)')
   
    #Network configuration
    #got it
    got_it_pv = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Got it")')
    #选择网关
    select_gateway = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageView").instance(0)')
    #选择优化器
    select_optimizer = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(10)')
    
    #Network configuration按钮
    network_configuration = (AppiumBy.CLASS_NAME, 'android.widget.Button')
    
    #设备添加结果
    result_device = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("1/1")')
    #exit按钮
    exit_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Exit")')
    
    #电站列表回到设备列表
    back_device_list = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(6)')
   
class AddLogicallayoutLocator:
    """添加逻辑布局页面的元素定位"""



class PlantListLocator:
    """进入电站页面元素定位"""
    #底部导航-plant
    plant = (AppiumBy.XPATH, "//android.view.View[contains(@content-desc, 'Plants')]")
    #搜索电站
    search_plant = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText")')
    #site_info = (By.XPATH, "//span[text()='新增电站']")
    #列表中第一个电站
    enter_plant = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageView").instance(0)')
   
class PlantinfoLocatorr:
    """电站详情元素定位"""
    #底部导航-Device
    Device = (AppiumBy.XPATH, "//android.view.View[contains(@content-desc, 'Device')]")
    #底部导航-Layout
    Layout = (AppiumBy.XPATH, "//android.view.View[contains(@content-desc, 'Layout')]")
    #底部导航-Analysis
    Analysis = (AppiumBy.XPATH, "//android.view.View[contains(@content-desc, 'Analysis')]")
    #底部导航-BasicInfo
    BasicInfo = (AppiumBy.XPATH, "//android.view.View[contains(@content-desc, 'Basic Info')]")
    
    #添加设备+ - 使用多种定位策略
    add_device = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Add Device")')
    # 备用定位器
    add_device_alt1 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Add Device")')
    add_device_alt2 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").description("Add Device")')
    add_device_alt3 = (AppiumBy.XPATH, "//android.view.View[contains(@content-desc, 'Add Device')]")
 
