import uuid
from datetime import datetime, timedelta, timezone
from lib.db import db, Db
from lib.cognito_verification import jwt_verifier

class CreateActivity:
  @staticmethod
  def run(request):
    model = {
      'errors': {
        'message': None,
        'status': None
      },
      'data': None
    }

    authenticated = jwt_verifier.accept_request_headers(request.headers)
    if authenticated is None:
      model['errors']['message'] = "You need to be authenticated to public cruds"
      model['errors']['status'] = 401
      return model
    message = request.get_json()["message"]
    ttl = request.get_json()["ttl"]

    sql = """
          INSERT INTO activities()
          """

    now = datetime.now(timezone.utc).astimezone()

    if (ttl == '30-days'):
      ttl_offset = timedelta(days=30) 
    elif (ttl == '7-days'):
      ttl_offset = timedelta(days=7) 
    elif (ttl == '3-days'):
      ttl_offset = timedelta(days=3) 
    elif (ttl == '1-day'):
      ttl_offset = timedelta(days=1) 
    elif (ttl == '12-hours'):
      ttl_offset = timedelta(hours=12) 
    elif (ttl == '3-hours'):
      ttl_offset = timedelta(hours=3) 
    elif (ttl == '1-hour'):
      ttl_offset = timedelta(hours=1) 
    else:
      model['errors'] = ['ttl_blank']

    if user_handle == None or len(user_handle) < 1:
      model['errors'] = ['user_handle_blank']

    if message == None or len(message) < 1:
      model['errors'] = ['message_blank'] 
    elif len(message) > 280:
      model['errors'] = ['message_exceed_max_chars'] 

    if model['errors']:
      model['data'] = {
        'nickname':  user_handle,
        'message': message
      }   
    else:
      model['data'] = {
        'uuid': uuid.uuid4(),
        'display_name': 'Andrew Brown',
        'handle':  user_handle,
        'message': message,
        'created_at': now.isoformat(),
        'expires_at': (now + ttl_offset).isoformat()
      }
    return model