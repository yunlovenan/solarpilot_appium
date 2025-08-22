from selenium.webdriver.common.by import By


class DeviceAddLocator:
    """添加设备页面的元素定位"""
    # 菜单设备
    device = (By.XPATH, "//*[contains(text(), '设备')]")
    # 新增设备按钮
    device_add = (By.XPATH, "//span[text()='新增设备']")
    #添加网关/采集器设备
    device_add_gateway = (By.XPATH, "//div[text()='添加网关/采集器设备']")
    #设备sn
    device_sn = (By.ID, "devices_0_deviceSn")
    #设备名称
    device_name = (By.ID, "devices_0_deviceName")
    #添加并激活
    device_add_and_active = (By.XPATH, "//span[text()='添加并激活']")
    
    #激活结果
    device_active_success = (By.CLASS_NAME, "vpp-device-active-result-item-right-count")
    #激活失败
    device_active_fail = (By.CLASS_NAME, "vpp-device-active-result-item-right")
    
    #确定
    device_confirm = (By.XPATH, "//span[text()='确 定']")
    


class DevicelistLocator:
    """设备列表页面的元素定位"""
    
    # 设备名称输入框
    device_name_input = (By.XPATH, "//input[@placeholder='请输入设备名称']")
   
    # 列表中的第一个设备名称
    device_name_1 = (By.XPATH, '//tr[@class="cy-table-row cy-table-row-level-0"][1]/td/div/div/div/a')
    
    # 编辑按钮
    device_edit = (By.XPATH, '//tr[@class="cy-table-row cy-table-row-level-0"][1]/td[7]/a')
    
    
    
   


class DeviceinfoLocator:
    """设备详情页面的元素定位"""
    