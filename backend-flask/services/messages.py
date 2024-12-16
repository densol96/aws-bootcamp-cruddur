from datetime import datetime, timedelta, timezone
from lib.ddb import ddb 

class Messages:
  def run(user_sub, group_uuid):
    model = {
        'errors': None,
        'data': None
      }

    ##### TODO: Authorization
    # sql = db.load_sql_script("users", "uuid_from_sub.sql")
    # user_uuid = db.sql_query(sql, {"cognito_user_id": sub})
   
    # if user_uuid is not None:
      # results = ddb.list_messages_in_chat(group_chat_uuid)
      # model["data"] = results
    # else:
    #   print(f"No db-records for the user with the sub of {sub}")
    #   model["error"] = "Service currently unavailable"


    results = ddb.list_messages_in_chat(group_uuid)
    model["data"] = results
    return model