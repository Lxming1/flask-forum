from db.dbUtil import MysqlPool
from utils.handle_pas import handlePas


class DbUser:

  def dbLogin(self, username, password):
    password = handlePas(password)
    mySelf = MysqlPool().getConnect()
    sql = "select * from users where name = %s and password = %s"
    mySelf.cursor.execute(sql, (username, password))
    result = mySelf.cursor.fetchall()
    if result:
      return result[0]
    else:
      return []

  def dbRegister(self, username, password):
    password = handlePas(password)
    mySelf = MysqlPool().getConnect()
    sql = "insert into users(name, password) values (%s, %s)"
    mySelf.cursor.execute(sql, (username, password))
    mySelf.conn.commit()
    mySelf.closeConnect()

  def delAvatar(self, userId):
    mySelf = MysqlPool().getConnect()
    sql = "select filename from avatar where user_id = %s"
    mySelf.cursor.execute(sql, userId)
    result = mySelf.cursor.fetchall()
    if result != ():
      filename = result[0]['filename']
      sql = "update users set avatar_url = null where id = %s"
      mySelf.cursor.execute(sql, userId)
      mySelf.conn.commit()

      sql = "delete from avatar where user_id = %s"
      mySelf.cursor.execute(sql, (userId, ))
      mySelf.conn.commit()
      mySelf.closeConnect()
      return filename

    return ''

  def setAvatar(self, filePath, userId):
    mySelf = MysqlPool().getConnect()
    sql = "update users set avatar_url = %s where id = %s"
    mySelf.cursor.execute(sql, (filePath, userId))
    mySelf.conn.commit()
    mySelf.closeConnect()

  def updateUserMes(self, username, userId, password=''):
    mySelf = MysqlPool().getConnect()
    if password == '':
      sql = "update users set name = %s where id = %s"
      mySelf.cursor.execute(sql, (username, userId))
    else:
      password = handlePas(password)
      sql = 'update users set name = %s, password = %s where id = %s'
      mySelf.cursor.execute(sql, (username, password, userId))
    mySelf.conn.commit()
    mySelf.closeConnect()


