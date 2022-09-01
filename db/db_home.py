from db.dbUtil import MysqlPool
from utils.handle_pas import handlePas


class DbHome:
  def getMomment(self):
    mySelf = MysqlPool().getConnect()
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
      GROUP BY m.id ORDER BY m.id desc
    '''
    mySelf.cursor.execute(sql)
    result = mySelf.cursor.fetchall()
    if result:
      return result
    else:
      return []

  def register(self, username, password):
    password = handlePas(password)
    mySelf = MysqlPool().getConnect()
    sql = "insert into users(name, password) values (%s, %s)"
    mySelf.cursor.execute(sql, (username, password))
    result = mySelf.cursor.fetchall()
    if result:
      return result[0]
    else:
      return []