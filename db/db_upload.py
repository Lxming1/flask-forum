from db.dbUtil import MysqlPool


class DbUpload:

  def dbSaveAvatar(self, filename, mimetype, size, user_id):
    mySelf = MysqlPool().getConnect()
    sql = "insert into avatar (filename, mimetype, size, user_id) values (%s, %s, %s, %s)"
    mySelf.cursor.execute(sql, (filename, mimetype, size, user_id))
    mySelf.conn.commit()
    mySelf.closeConnect()

