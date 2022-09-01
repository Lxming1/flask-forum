import pymysql
from dbutils.pooled_db import PooledDB

from utils.config import MYSQL_HOST, MYSQL_USER, MYSQL_DATABASES, MYSQL_PASSWORD


class MysqlPool:
  config = {
      'creator': pymysql,
      'host': MYSQL_HOST,
      'user': MYSQL_USER,
      'password': MYSQL_PASSWORD,
      'db': MYSQL_DATABASES,
      'maxconnections': 70,  # 连接池最大连接数量
      'cursorclass': pymysql.cursors.DictCursor
  }
  pool = PooledDB(**config)

  def getConnect(self):
    self.conn = MysqlPool.pool.connection()
    self.cursor = self.conn.cursor()
    return self

  def closeConnect(self):
    self.cursor.close()
    self.conn.close()
