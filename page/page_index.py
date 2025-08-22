
from common.base_page import BasePage
from locator.locator_index import IndexLocator as loc


class IndexPage(BasePage):
    """首页"""

    def get_my_user_info(self):
        """获取信息"""
        try:
            self.get_element(loc.index, '综合概览')
        except: # 如果找不到元素，则返回登录失败
            return '登录失败'
        else:
            return '登录成功'

   



    

