import pymysql
from common.handle_config import conf

class HandleMysql:
    """操作mysql数据库的类"""

    def __init__(self):
        """初始化方法中，连接到数据库"""
        # 建立连接
        self.con = pymysql.connect(host=conf.get("mysql", "host"),
                                   port=conf.getint("mysql", "port"),
                                   user=conf.get("mysql", "user"),
                                   password=conf.get("mysql", "password"),
                                   charset="utf8",
                                   database = "energy_app_middle_test",#数据库名称
                                   cursorclass=pymysql.cursors.DictCursor
                                   )
        # 创建一个游标对象
        self.cur = self.con.cursor()

    def find_all(self, sql):
        """
        查询sql语句返回的所有数据
        :param sql: 查询的sql
        :return: 查询到的所有数据
        """
        self.con.commit()
        self.cur.execute(sql)
        return self.cur.fetchall()

    def find_one(self, sql):
        """
        查询sql语句返回的第一条数据
        :param sql: 查询的sql
        :type sql:str
        :return: sql语句查询到的第一条数据
        """
        self.con.commit()
        self.cur.execute(sql)
        return self.cur.fetchone()

    def find_count(self, sql):
        """
        sql语句查询到的数据条数
        :param sql: 查询的sql
        :return:查询到的数据条数
        """
        self.con.commit()
        res = self.cur.execute(sql)
        return res

    def update(self, sql):
        """
        增删改操作的方法
        :param sql: 增删改的sql语句
        :return:
        """
        self.cur.execute(sql)
        self.con.commit()
    def inser_one(self,sql):
        "插入数据"
        self.cur.execute(sql)
        self.con.commit()
        
    def close(self):
        
        """断开游标，关闭连接"""
        self.cur.close()
        self.con.close()



# 延迟数据库连接，避免模块导入时就连接数据库
# db = HandleMysql()
# 
# #sql = "select ap.lte_bands,ap.nr_bands,ap.daily_lte_bands,ap.daily_nr_bands from antenna_param ap left join antenna an on an.id=ap.antenna_id  where an.number = 'an1702885877323'"
# #sql = "select *from detector where imei ='sn1703038719952'"
# #sql = "select *from antenna_band ap left join antenna a on ap.antenna_id=a.id where a.number ='1215'"
# #sql = "select *from antenna where number ='an1703129921651'"
# sql =  "select *from antenna_param ap left join antenna a on ap.antenna_id=a.id where a.number = 'an1703129796862'"
#sql = "select a.number,ap.learning_cycle from antenna_param ap left join antenna a on ap.antenna_id=a.id where ap.site_id = 13 and a.deleted = 0"
# number = 'an1703233162724'
# sql= "select *from antenna where number = '{}'".format(number)
# res = db.find_one(sql)
# res_id = res['id']
# 
# print(res_id)


