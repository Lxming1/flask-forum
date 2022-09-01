from string import Template

from db.dbUtil import MysqlPool


class DbMoment:

  def commonSql(self, conditions):
    sql = '''
      SELECT 
        m.id id, m.content content,
        IF(count(l.id), JSON_ARRAYAGG(
          JSON_OBJECT(
            'id', l.id,
            'name', l.name
          )
        ) , NULL) labels,
        (select count(*) from moment_label ml where ml.moment_id = m.id) labelCount,
        (select count(*) from comment ml where ml.moment_id = m.id) commentCount,

        JSON_OBJECT(
          'id', u.id, 
          'name', u.name, 
          'avatarUrl', u.avatar_url
        ) author, 
        m.createAt createTime, m.updateAt updataTime
      FROM moment m
      LEFT JOIN users u ON m.user_id = u.id
      LEFT JOIN moment_label ml ON ml.moment_id = m.id
      LEFT JOIN label l ON l.id = ml.label_id
      WHERE ${con}
      GROUP BY m.id ORDER BY m.id desc
    '''
    t = Template(sql)
    return t.substitute(con=conditions)

  def searchLabel(self, label):
    mySelf = MysqlPool().getConnect()
    sql = "select * from label where name = %s"
    mySelf.cursor.execute(sql, label)
    result = mySelf.cursor.fetchall()
    if result != ():
      return result[0]
    else:
      return {}

  def insertLabel(self, label):
    mySelf = MysqlPool().getConnect()
    sql = "insert into label (name) values (%s)"
    mySelf.cursor.execute(sql, (label))
    id = mySelf.cursor.lastrowid
    mySelf.conn.commit()
    mySelf.closeConnect()

    return id

  def insertMoment(self, content, userId):
    mySelf = MysqlPool().getConnect()
    sql = "insert into moment (content, user_id) values (%s, %s)"
    mySelf.cursor.execute(sql, (content, userId))
    id = mySelf.cursor.lastrowid
    mySelf.conn.commit()
    mySelf.closeConnect()
    return id

  def editMoment(self, content, userId, momentId):
    mySelf = MysqlPool().getConnect()
    sql = "update moment set content = %s where user_id = %s and id = %s"
    mySelf.cursor.execute(sql, (content, userId, momentId))
    mySelf.conn.commit()
    mySelf.closeConnect()

  def insertMomentAndLabel(self, momentId, labelId):
    mySelf = MysqlPool().getConnect()
    sql = "insert into moment_label (moment_id, label_id) values (%s, %s)"
    mySelf.cursor.execute(sql, (momentId, labelId))
    mySelf.conn.commit()
    mySelf.closeConnect()

  def delMomentAndLabel(self, momentId, labelId):
    mySelf = MysqlPool().getConnect()
    sql = "delete from moment_label where moment_id = %s and label_id = %s"
    mySelf.cursor.execute(sql, (momentId, labelId))
    mySelf.conn.commit()
    mySelf.closeConnect()

  def searchMoment(self, content):
    mySelf = MysqlPool().getConnect()
    sql = self.commonSql('content like %s')
    mySelf.cursor.execute(sql, ('%'+content+'%'))
    result = mySelf.cursor.fetchall()
    if result != ():
      return result
    else:
      return []

  def searchMomentByUser(self, username):
    mySelf = MysqlPool().getConnect()
    sql = self.commonSql('u.name like %s')
    mySelf.cursor.execute(sql, ('%' + username + '%'))
    result = mySelf.cursor.fetchall()
    if result != ():
      return result
    else:
      return []

  def searchMomentByLabel(self, label):
    mySelf = MysqlPool().getConnect()
    sql = self.commonSql('l.name like %s')
    mySelf.cursor.execute(sql, ('%' + label + '%'))
    result = mySelf.cursor.fetchall()
    if result != ():
      return result
    else:
      return []

  def profileMoment(self, userId):
    mySelf = MysqlPool().getConnect()
    sql = self.commonSql('user_id = %s')

    mySelf.cursor.execute(sql, userId)
    result = mySelf.cursor.fetchall()
    if result != ():
      return result
    else:
      return []

  def addComment(self, content, momentId, userId):
    mySelf = MysqlPool().getConnect()
    sql = 'insert into comment (content, moment_id, user_id) values (%s, %s, %s)'
    mySelf.cursor.execute(sql, (content, momentId, userId))
    mySelf.conn.commit()
    mySelf.closeConnect()

  def showComments(self, momentId):
    mySelf = MysqlPool().getConnect()
    sql = """
      SELECT 
        c.id id, c.content content, c.comment_id commentId,
        JSON_OBJECT('id', u.id, 'name', u.name, 'avatarUrl', u.avatar_url) author, 
        c.createAt createTime, c.updateAt updateTime 
      FROM comment c 
      LEFT JOIN users u
      ON c.user_id = u.id
      where c.moment_id = %s
    """
    mySelf.cursor.execute(sql, (momentId))
    result = mySelf.cursor.fetchall()
    if result != ():
      return result
    else:
      return []

  def addReplyComment(self, content, userId, momentId, commentId):
    mySelf = MysqlPool().getConnect()
    sql = 'insert into comment (content, moment_id, user_id, comment_id) values (%s, %s, %s, %s)'
    mySelf.cursor.execute(sql, (content, momentId, userId, commentId))
    mySelf.conn.commit()
    mySelf.closeConnect()

  def delComment(self, commentId):
    mySelf = MysqlPool().getConnect()
    sql = 'delete from comment where id = %s'
    mySelf.cursor.execute(sql, (commentId))
    mySelf.conn.commit()
    mySelf.closeConnect()

  def getLabelId(self, labelName):
    mySelf = MysqlPool().getConnect()
    sql = 'select id from label where name = %s'
    mySelf.cursor.execute(sql, (labelName))
    result = mySelf.cursor.fetchall()
    return result[0]['id']

  def delMoment(self, momentId):
    mySelf = MysqlPool().getConnect()
    sql = 'delete from moment where id = %s'
    mySelf.cursor.execute(sql, (momentId))
    mySelf.conn.commit()
    mySelf.closeConnect()