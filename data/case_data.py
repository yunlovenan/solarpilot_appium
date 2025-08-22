
class LoginCase:
    """登录功能的用例数据"""
    # 正常登录的用例
    success_case_data = [
        {'username': "mayunfws", "pwd": "mayun1314@", "expected": "登录成功"},
    ]
    # 异常的用例数据：错误提示在页面上
    error_case_data = [
        {'username': "mayunfws", "pwd": "123456", "expected": "账号密码错误"},
    ]

class SiteCase:
    success_case_data = [
        {'sitename': "lihaiying123", "number": "a123456", "addrno": "a123456","contact": "li","phone": "18067988320","siteaddress": "利尔达物联网科技园"},
    ]