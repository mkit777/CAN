import pymysql
from contextlib import contextmanager

class Auto_Storage:
    def __init__(self, con, sql, capacity, has_handler=False):
        self.con = con
        self.sql = sql
        self.storage_capacity = capacity
        self.has_handler = has_handler
        self.storage = []
    
    def store(self, item):
        if self.has_handler:
            item = item.db_handler()
        self.storage.append(item)
        if len(self.storage) >= self.storage_capacity:
            self.commit()

    def commit(self):
        try:
            cur = self.con.cursor()
            cur.executemany(self.sql, self.storage)
            self.con.commit()
            self.storage = []
        except Exception as e:
            self.con.rollback()
            raise e
        finally:
            cur.close()


class DBClinet:
    def __init__(self, host, user, password, database, port):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.con = None

    def get_connection(self):
        if self.con is None:
            self.con = pymysql.connect(self.host, self.user, self.password, self.database, self.port)
        return self.con

    def get_auto_storage(self, capacity, sql,has_handler=False):
        '''
        自动提交仓库
        Parameters:
        capacity: 容量
        sql: 语句
        '''
        con = self.get_connection()
        return Auto_Storage(self.con, sql, capacity, has_handler)