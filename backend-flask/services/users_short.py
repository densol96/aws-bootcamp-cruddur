from lib.db import db

class UsersShort:
  def run(nickname):
    sql = db.load_sql_script('users','user_short_from_nickname.sql')
    results = db.query_object_json(sql,{
      'nickname': nickname
    })
    return results