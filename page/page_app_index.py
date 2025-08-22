
from common.base_page import BasePage
from locator.locator_app_login import APPLoginLocator as app_loc
from appium.webdriver.common.appiumby import AppiumBy
import time


class APPIndexPage(BasePage):
    """登录成功验证Me"""

    def get_me_info(self):
        """通过首页特征或登录控件消失来判定是否登录成功"""
        try:
            # 等待页面稳定
            time.sleep(2)

            # 1) 若登录按钮还在，判定失败
            if self.is_element_exist(app_loc.login_loc):
                return '登录失败'

            # 2) 多个首页候选特征，任意一个出现即可判定成功
            candidate_locators = [
                (AppiumBy.ACCESSIBILITY_ID, 'Me'),
                (AppiumBy.XPATH, "//android.view.View[contains(@content-desc, 'Me')]") ,
                (AppiumBy.XPATH, "//android.view.View[contains(@content-desc, 'Plants')]") ,
                (AppiumBy.XPATH, "//android.view.View[contains(@content-desc, 'Device')]") ,
                (AppiumBy.XPATH, "//android.view.View[contains(@content-desc, 'Home')]") ,
            ]

            for locator in candidate_locators:
                if self.is_element_exist(locator):
                    return '登录成功'

            # 3) 再次等待后重试
            time.sleep(3)
            if not self.is_element_exist(app_loc.login_loc):
                return '登录成功'

            return '登录失败'
        except Exception:
            return '登录失败'

   



    

