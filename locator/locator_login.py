
from selenium.webdriver.common.by import By


class LoginLocator:
    """登录页面的元素定位"""
    # 账号输入框
    username_loc = (By.CSS_SELECTOR, 'input[type="text"]')
    # 密码输入框
    pwd_loc = (By.CSS_SELECTOR, 'input[type="password"]')
    # 服务条款复选框
    service_loc = (By.CSS_SELECTOR, 'input[type="checkbox"]')
    # 点击按钮
    login_loc = (By.XPATH, "//span[text()='登 录']")
    # 失败的提示内容
    error_info = (By.XPATH, "//div[@class='cy-message-error']")
    # 点击我是服务商
    me_service = (By.XPATH, "//*[contains(text(), '我是服务商')]")
    # 备用定位器
    me_service_alt = (By.XPATH, "//span[contains(text(), '我是服务商')]")
    me_service_alt2 = (By.XPATH, "//button[contains(text(), '我是服务商')]")
    me_service_alt3 = (By.XPATH, "//div[contains(text(), '我是服务商')]")
    