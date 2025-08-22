
from selenium.webdriver.common.by import By


class IndexLocator:
    """首页的元素定位"""
    # 用户信息
    user_info = (By.XPATH, "//*[contains(text(),'长园飞轮')]")
    index = (By.XPATH, "//*[contains(text(), '综合概览') or contains(text(), '光伏运营')]")



