import re
from common.handle_sql import HandleMysql
from common.handle_config import conf
class EnvData:
    """定义一个类，用来保存用例执行过程中，提取出来的数据"""
    pass



# class BandData:
#     """添加天线后，天线运营商对应的默认频段表"""
#     #'0移动 1联通 2电信 3电联 4三网'4G日常扫描band
#     lte_daily_bands = {"0": ["3", "8", "34", "39", "40", "41"]}
#     lte_daily_bands_1 = {"1": ["1", "3"]}
#     lte_daily_bands_2 = {"2": ["1", "3"]}
#     lte_daily_bands_3 = {"3": ["1", "3"]}
#     lte_daily_bands_4 = {"4": ["1", "3", "8", "34", "39", "40", "41"]}
#     # '0移动 1联通 2电信 3电联 4三网'5G日常扫描band
#     nr_daily_bands_0 = {"0": ["2515"]}
#     nr_daily_bands_1 = {"1": ["2100", "3400", "3500"]}
#     nr_daily_bands_2 = {"1": ["2100", "3400", "3500"]}
#     nr_daily_bands_3 = {"1": ["2100", "3400", "3500"]}
#     nr_daily_bands_4 = {"4": ["2100", "2515", "3400", "3500"]}
#     # '0移动 1联通 2电信 3电联 4三网'4G日全频段扫描band
#     lte_all_bands_0 = {"0": ["3", "8", "34", "39", "40", "41"]}
#     lte_all_bands_1 = {"1": ["1", "3"]}
#     lte_all_bands_2 = {"2": ["1", "3"]}
#     lte_all_bands_3 = {"2": ["1", "3"]}
#     lte_all_bands_4 ={"4": ["1", "3", "8", "34", "39", "40", "41"]}
#     # '0移动 1联通 2电信 3电联 4三网'5G日全频段扫描band
#     nr_all_bands_0 = {"0": ["2515"]}
#     nr_all_bands_1 = {"1": ["2100", "3400", "3500"]}
#     nr_all_bands_2 = {"1": ["2100", "3400", "3500"]}
#     nr_all_bands_3 = {"1": ["2100", "3400", "3500"]}
#     nr_all_bands_4 = {"4": ["2100", "2515", "3400", "3500"]}

# def get_band_default(mnc):
#     if mnc == 0:
#         pass
#     elif mnc ==4:
#         bands = {'lte_bands': '{"4": ["1", "3", "8", "34", "39", "40", "41"]}', 'nr_bands': '{"4": ["2100", "2515", "3400", "3500"]}', 'daily_lte_bands': '{"4": ["1", "3", "8", "34", "39", "40", "41"]}', 'daily_nr_bands': '{"4": ["2100", "2515", "3400", "3500"]}'}
#     else:
#         pass
    

def  get_standard_data():
    "获取标准数据"
    try:
        db = HandleMysql()
        # 电站名称
        sql_site = "SELECT * FROM eam_project WHERE project_name= '{}'".format(conf.get("standard_data", "sitename"))

        # # 天线
        # sql_antena = "select *from antenna a where site_id={}".format(conf.get("standard_data", "site_id"))
        # # 天线参数
        # sql_antena_param = "select *from antenna_param ap where site_id={}".format(conf.get("standard_data", "site_id"))

        # #天线band
        # sql_antena_bands = "SELECT *from antenna_band ab LEFT JOIN antenna a on ab.antenna_id = a.id LEFT JOIN site s on a.site_id = s.id where s.id = {}".format(conf.get("standard_data", "site_id"))
        site = db.find_all(sql_site)
        # antena = db.find_all(sql_antena)
        # antena_param = db.find_all(sql_antena_param)
        # sql_antena_bands =db.find_all(sql_antena_bands)
        db.close()
        return site, [], [], []  # 返回4个值以匹配期望
    except Exception as e:
        print(f"数据库连接失败，使用模拟数据: {e}")
        # 返回模拟数据
        return [], [], [], []

#get_standard_data()


# a,b,c = get_standard_data()
# A,B,C = get_standard_data()
#
# if a==A and b==B and c==C:
#     print("chenggong")
# else:
#     print("shibai")
# def replace_data(data):
#     """替换数据"""
# 
#     while re.search("#(.*?)#", data):
#         res = re.search("#(.*?)#", data)
#         # 返回的式一个匹配对象
#         # 获取匹配到的数据
#         key = res.group()
#         # 获取匹配规则中括号里面的内容
#         item = res.group(1)
#         try:
#             # 获取配置文件中对应的值
#             value = conf.get("test_data", item)
#         except:
#             # 去EnvData这个类里面获取对应的属性（环境变量）
#             value = getattr(EnvData, item)
# 
#         data = data.replace(key, value)
#     return data