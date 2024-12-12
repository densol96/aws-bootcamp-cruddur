import uuid
from datetime import datetime, timedelta, timezone
from lib.db import db, Db
from lib.cognito_verification import jwt_verifier

class CreateActivity:
  model = {
      'errors': {
        'message': None,
        'status': None
      },
      'data': None
    }

  @staticmethod
  def run(request):
    ## for better readability
    cognito_user_id = jwt_verifier.extract_cognito_user_id(request)
    if cognito_user_id is None:
      CreateActivity.model['errors']['message'] = "You are not authenticated"
      CreateActivity.model['errors']['status'] = 401
      return CreateActivity.model
    
    message = CreateActivity.extract_message(request)
    if message is None:
      return CreateActivity.model

    expires_at = CreateActivity.extract_expires_at(request)
    if expires_at is None:
      return CreateActivity.model
    
    sql = Db.load_sql_script("activities", "create.sql")
    new_activity = db.sql_query(sql, {"cognito_user_id": cognito_user_id, "message": message, "expires_at": expires_at})
    if new_activity is None:
      CreateActivity.model['errors']['message'] = "Service is currently unavailable"
      CreateActivity.model['errors']['status'] = 500
    else:
      CreateActivity.model['data'] = new_activity
      CreateActivity.model['errors'] = None
    return CreateActivity.model

  @staticmethod
  def extract_message(request):
    message = request.get_json()["message"]
    if message == None or len(message) < 1:
      CreateActivity.model['errors']['message'] = ['message_blank'] 
      CreateActivity.model['errors']['status'] = 400
      message = None
    elif len(message) > 280:
      CreateActivity.model['errors']['message'] = ['message_exceed_max_chars']
      CreateActivity.model['errors']['status'] = 400 
      message = None 
    return message

  @staticmethod
  def extract_expires_at(request):
    ttl = request.json['ttl']
    if ttl is None:
      CreateActivity.model['errors'] = ['ttl_blank']
      CreateActivity.model['errors']['status'] = 400  
      return None
    
    now = datetime.now(timezone.utc).astimezone()
    ttl_offset = None
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
    
    if ttl_offset is not None:
      return now + ttl_offset
    CreateActivity.model['errors']['message'] = ['ttl invalid']
    CreateActivity.model['errors']['status'] = 400 
    return None
