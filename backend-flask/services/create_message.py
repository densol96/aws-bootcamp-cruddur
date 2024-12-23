from datetime import datetime, timedelta, timezone

from lib.db import db
from lib.ddb import ddb 

class CreateMessage:
  # mode indicates if we want to create a new message_group or using an existing one
  def run(mode, message, cognito_user_id, message_group_uuid=None, user_receiver_nickname=None):
    model = {
      'errors': None,
      'data': None
    }

    if (mode == "update"):
      if message_group_uuid == None or len(message_group_uuid) < 1:
        model['errors'] = ['message_group_uuid_blank']
    if cognito_user_id == None or len(cognito_user_id) < 1:
      model['errors'] = ['cognito_user_id_blank']
    if (mode == "create"):
      if user_receiver_nickname == None or len(user_receiver_nickname) < 1:
        model['errors'] = ['user_receiver_nickname_blank']
    if message == None or len(message) < 1:
      model['errors'] = ['message_blank'] 
    elif len(message) > 1024:
      model['errors'] = ['message_exceed_max_chars']

    short_sql = db.load_sql_script('users','user_short_from_sub.sql')  
    user_sender = db.query_object_json(short_sql, {"cognito_user_id": cognito_user_id})

    if model['errors']:
      # return what we provided
      model['data'] = {
        'name': user_sender["name"],
        'nickname': user_sender["nickname"],
        'message': message
      }
    else:
      if user_receiver_nickname == None:
        rev_handle = ''
      else:
        rev_handle = user_receiver_nickname
      sql = db.load_sql_script('users','create_message_users.sql')
      users = db.query_array_json(sql,{
        'cognito_user_id': cognito_user_id,
        'user_receiver_nickname': rev_handle
      })
      my_user    = next((item for item in users if item["kind"] == 'sender'), None)
      other_user = next((item for item in users if item["kind"] == 'recv')  , None)

      if (mode == "update"):
        data = ddb.create_message(
          message_group_uuid=message_group_uuid,
          message=message,
          my_user_uuid=my_user['uuid'],
          my_user_display_name=my_user['name'],
          my_user_handle=my_user['nickname']
        )
      elif (mode == "create"):
        data = ddb.create_message_group(
          message=message,
          my_user_uuid=my_user['uuid'],
          my_user_display_name=my_user['name'],
          my_user_handle=my_user['nickname'],
          other_user_uuid=other_user['uuid'],
          other_user_display_name=other_user['name'],
          other_user_handle=other_user['nickname']
        )
      if data is not None:
        model['data'] = data
      else:
        model['errors'] = ['Service currently unavailable']
    return model