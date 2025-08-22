from selenium.webdriver.common.by import By


class AntenaAddLocator:
    """添加天线页面的元素定位"""
    # 站点
    siteId = (By.XPATH, '//input[@id="siteId"]')
    siteId_0= (By.XPATH, '//div[@id="siteId_list_0"]')
    # 运营商
    mnc = (By.XPATH, '//input[@id="mnc"]')
    #移动
    mnc_select_1 = (By.XPATH, '//div[@class="rc-virtual-list-holder-inner"]/div[1]')
    #联通
    mnc_select_2 = (By.XPATH, '//div[@class="rc-virtual-list-holder-inner"]/div[2]')
    # 电信
    mnc_select_3 = (By.XPATH, '//div[@class="rc-virtual-list-holder-inner"]/div[3]')
    #电联
    mnc_select_4 = (By.XPATH, '//div[@class="rc-virtual-list-holder-inner"]/div[4]')
    #三网
    mnc_select_5 = (By.XPATH, '//div[@class="rc-virtual-list-holder-inner"]/div[5]')

    #天线编号
    antena_num = (By.XPATH, '//input[@id="number"]')
    #位置
    antena_position = (By.XPATH, '//input[@id="position"]')
    #监测终端
    antenna_detectorId = (By.XPATH, '//input[@id="detectorId"]')
    antenna_detectorId_0 = (By.XPATH, '//div[@id="detectorId_list_0"]')
    #上传图片
    antenna_pic_ = (By.XPATH, "//input[@tabindex='0'][contains(.,'上传')]")
    antenna_pic = (By.XPATH, "//input[@type='file']")
    #提交
    antenna_submit= (By.XPATH,"//button[@type='submit'][contains(.,'提交')]")


class AntennalistLocator:
    """天线列表页面的元素定位"""
    #菜单监测管理
    menu_moniter = (By.XPATH, "//span[text()='监测管理']")
    #菜单室分天线
    menu_antenna = (By.XPATH, "//span[text()='室分天线']")
    #添加天线按钮
    antenna_add = (By.XPATH, "//button[@class='ant-btn css-1rfaze7 ant-btn-default add___wML69']")

    #天线名称搜索框
    antenna_search = (By.XPATH, "//input[@id='search']")
    antenna_search_clear = (By.XPATH, "//span[@class='ant-input-clear-icon']")

    #列表天线
    antenna = (By.XPATH, "//a[@class='link___Ym13x']")

    #列表-编辑按钮
    antenna_edit = (By.XPATH, "//span[text()='编辑']")
    #列表-详情按钮
    antenna_info = (By.XPATH, "//span[text()='详情']")

    #列表-删除按钮
    antenna_delete = (By.XPATH, "//span[text()='删除']")
    # 弹框-确定删除按钮
    antenna_delete_re = (By.XPATH, "//span[text()='确 定']")





class AntenaInfoLocator:
    """天线详情页面的元素定位"""

    #tab
    # 参数配置按钮
    antenna_param = (By.XPATH, "//div[@data-node-key='tab4']")

    #基础配置
    basic_tab =  (By.XPATH, "//div[text()='基础配置']")
    #自学习信号阈值
    learningThreshold = (By.XPATH, "//input[@id='learningThreshold']")
    # 自学习周期
    learningCycle = (By.XPATH, "//input[@id='learningCycle']")
    # 自学习信号输入框删除按钮
    remove = (By.XPATH, "//span[@class='ant-input-clear-icon']")
    
    #自学习次数
    learningTimes = (By.XPATH, "//input[@id='learningTimes']")
    #LTE监测周期
    normalPeriod = (By.XPATH, "//input[@id='normalPeriod']")
    #5G监测周期
    normalPeriodCoefficient =  (By.XPATH, "//input[@id='normalPeriodCoefficient']")
    #衰减器开关开
    switch = (By.XPATH,"//input[@class ='ant-radio-input'and @value='0']")

    #频段配置
    bands_tab = (By.XPATH, "//div[text()='频段配置']")

    # 频段框,多个
    all_band_input = (By.XPATH, "//div[@class ='ant-select-selection-overflow']")
    # 频段的删除按钮
    band_remove = (By.XPATH, "//span[@class='ant-select-selection-item-remove']")
    #日常LTE扫描Band

    #日常5G扫描Band

    #全频段LTE扫描Band

    #全频段5G扫描Band



    #tab监测终端
    detector_tab =(By.XPATH, "//div[@data-node-key='tab3']")
    detector_change = (By.XPATH, "//span[text()='更换']")
    detector_change_confirm = (By.XPATH, "//span[text()='确定']")
    detector_input = (By.XPATH, "//div[@class='ant-select css-1rfaze7 ant-select-single ant-select-show-arrow ant-select-show-search']/div/span/input")
    
    #tab 频段信息
    bandinfo_tab = (By.XPATH, "//div[@data-node-key='tab1']")
    reset_bands = (By.XPATH, "//span[text()='重置监测频段']")
    con_reset_bands = (By.XPATH, "//span[text()='确 定']")

    submit = (By.XPATH, "//button[@type='submit']")