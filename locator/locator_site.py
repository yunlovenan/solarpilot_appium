from selenium.webdriver.common.by import By


class SiteAddLocator:
    """添加站点页面的元素定位"""
    # 电站名称
    site_name = (By.ID, 'name')
    # 电站类型
    site_type = (By.ID, 'powerStationType')
    #户用/工商业
    #type_select =  (By.XPATH, '//div[@class="cy-select-selection-item"][contains(.,"户用")]')
    # 系统类型
    site_system = (By.ID, 'energyType')
    # 选择光伏
    #system_select =  (By.XPATH, '//input[@id="energyType"][contains(.,"光伏")]')
    # 装机功率
    site_capacity = (By.ID, 'seriesCapacity')
    #国家/地区
    site_country = (By.ID, 'countryCode')
    #选择中国
   # country_select =  (By.XPATH, '//div[@id="countryCode"][contains(.,"中国")]')
    #经纬度
    site_map = (By.ID, 'mapPosition')
    # 电站地址
    site_address = (By.XPATH, "//div[@class='m-input-N2PpBt']/span/input")
    #选择地址
    site_address_select = (By.XPATH, '//div[@class="m-content-WiAcA1"]')
    # 确定
    site_confirm = (By.XPATH, "//span[text()='确 定']")

    # 联系人
    contact = (By.ID, 'contactName')
    # 联系电话
    phone = (By.XPATH, '//input[@id="contactNumber"]')
    #下一步
    site_next = (By.XPATH, "//span[text()='下一步']")
    
    #电价配置
    site_price = (By.XPATH, "//input[@role='spinbutton']")
     #下一步
    site_next = (By.XPATH, "//span[text()='下一步']")
    
    #完成
    site_complete = (By.XPATH, "//button[@class='cy-btn cy-btn-primary']")
    
    # #站点区域
    # site_area = (By.ID, 'region')


    # province_select =  (By.XPATH, '//div[@class="ant-cascader-menu-item-content"][contains(.,"浙江省")]')
    # city_select =  (By.XPATH, '//div[@class="ant-cascader-menu-item-content"][contains(.,"杭州市")]')
    # district_select = (By.XPATH, '//div[@class="ant-cascader-menu-item-content"][contains(.,"余杭区")]')

    # #站点地址
    # site_address =(By.XPATH, '//input[@id="tipAddress"]')

    # addresslist = (By.XPATH, '//div[@id="amap-sug0"][1]')
    # #站点GPS
    # site_gps = (By.XPATH, '//input[@id="gps"]')

    # #地图
    # site_amap = (By.XPATH, '//div[@class="amap-container"]')

    # submitbutton  = (By.XPATH, '//button[@type="submit"][contains(.,"提交")]')


class SitelistLocator:
    #菜单站点管理
    site = (By.XPATH, "//*[contains(text(), '电站列表')]")
    #菜单站点信息管理
    #site_info = (By.XPATH, "//span[text()='新增电站']")
    #添加站点按钮
    site_add = (By.XPATH, "//span[text()='新增电站']")

    #站点名称搜索框
    site_search = (By.XPATH, "//input[@class='cy-input']")
    site_search_clear =  (By.CSS_SELECTOR, "input[value=""]")

    #列表的第一个电站名称
    sitename_1 = (By.XPATH, '//td[@class="cy-table-row cy-table-row-level-0"][1]')

    #查看按钮（列表中第一条）
    #site_details = (By.XPATH, "//tbody[@class='cy-table-tbody']/tr[2]/td[11]/div/div/span/a")
    site_details = (By.XPATH, "//td[@class='cy-table-cell cy-table-cell-fix-right cy-table-cell-fix-right-first'][1]/div/div/span/a")
    #关于电站
    site_about = (By.XPATH, "//*[contains(text(), '关于电站')]")
    site_edit = (By.XPATH, "//span[text()='更新基本信息']")

    # 删除电站
    site_delete = (By.XPATH, "//span[contains(text(),'删 除')]")
    # 列表操作按钮--删除
    site_delete_confirm = (By.XPATH, "//span[text()='确 定']")
    #二次确认
    site_delete_confirm_2 = (By.XPATH, "//span[text()='继续删除']")

class SiteinfoLocator:
   "站点详情页元素"

   #重置监测频段
   site_reset_bands = (By.XPATH, "//span[text()='重置监测频段']")

   # 重置监测频段-确定
   site_reset_bands_confirm = (By.XPATH, "//span[text()='确 定']")

   #tab参数配置
   site_param_tab = (By.XPATH, "//div[text()='参数设置']")

    #基础配置
   site_basic_param = (By.XPATH, "//div[text()='基础配置']")

   # 自学习信号阈值
   site_learningThreshold = (By.XPATH, "//input[@id='learningThreshold']")
   # 自学习周期
   site_learningCycle = (By.XPATH, "//input[@id='learningCycle']")

   # 输入框删除按钮,会定位到多个
   site_param_remove = (By.XPATH, "//span[@class='ant-input-clear-icon']")

   # 自学习次数
   site_learningTimes = (By.XPATH, "//input[@id='learningTimes']")
   # LTE监测周期
   site_normalPeriod = (By.XPATH, "//input[@id='normalPeriod']")
   # 5G监测周期
   site_normalPeriodCoefficient = (By.XPATH, "//input[@id='normalPeriodCoefficient']")
   # 衰减器开关开
   site_switch = (By.XPATH, "//input[@class ='ant-radio-input'and @value='0']")

   site_submit =  (By.XPATH, "//button[@type='submit']")
   # 频段配置
   site_bands = (By.XPATH, "//div[text()='频段配置']")
   # 频段框,多个
   site_all_band = (By.XPATH, "//div[@class ='ant-select-selection-overflow']")
   # 频段的删除按钮
   band_remove = (By.XPATH, "//span[@class='ant-select-selection-item-remove']")


   # 日常LTE扫描Band

   # 日常5G扫描Band

   # 全频段LTE扫描Band

   # 全频段5G扫描Band

   # 告警配置
   site_warning = (By.XPATH, "//div[text()='告警规则']")
