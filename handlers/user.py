# coding=utf8
# @author: Arthas

from handlers.base import BaseHandler
from component.utils import make_response
from config.config import StatusCode
import pymysql


class UserHandler(BaseHandler):
    async def get_user_list(self):
        db = pymysql.connect(host='localhost',
                     user='root',
                     password='Lixinleonhardt3',
                     database='frozen_throne')
 
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        
        # 使用 execute()  方法执行 SQL 查询 
        cursor.execute("SELECT * from user")
        
        # 使用 fetchone() 方法获取单条数据.
        data = cursor.fetchall()
        
        print(type(data))
        print(type(data[0]))
        
        # 关闭数据库连接
        db.close()

        return make_response(StatusCode.success, arg={"content": "hello world"})





