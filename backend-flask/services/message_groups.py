from datetime import datetime, timedelta, timezone
from lib.ddb import ddb 
from lib.db import db 

class MessageGroups:
  def run(sub):
    model = {
      'errors': None,
      'data': None
    }
    sql = db.load_sql_script("users", "uuid_from_sub.sql")
    uuid = db.sql_query(sql, {"cognito_user_id": sub})
    if uuid is not None:
      results = ddb.list_message_groups(uuid)
      print("results: ", uuid, results)
      model["data"] = results
    else:
      print(f"No db-records for the user with the sub of {sub}")
      model["error"] = "Service currently unavailable"
    return model