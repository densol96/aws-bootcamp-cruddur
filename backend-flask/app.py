from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import os

from services.home_activities import *
from services.user_activities import *
from services.create_activity import *
from services.create_reply import *
from services.search_activities import *
from services.message_groups import *
from services.messages import *
from services.create_message import *
from services.show_activity import *
from services.notifications_activities import *

# Homeycomb related stuff
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# AWS xray
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

# AWS CloudWatch Logs
import watchtower
import logging
from time import strftime

# Custom JWT verifier using Cognito public key
from lib.cognito_verification import jwt_verifier

# Initialize tracing and an exporter that can send data to Honeycomb
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

app = Flask(__name__)

# More honeycomb
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

# AWS xray
xray_url = os.getenv("AWS_XRAY_URL")
xray_recorder.configure(service='Cruddur', dynamic_naming=xray_url)
XRayMiddleware(app, xray_recorder)

# Configuring Logger to Use CloudWatch
# LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.DEBUG)
# console_handler = logging.StreamHandler()
# cw_handler = watchtower.CloudWatchLogHandler(log_group='cruddur')
# LOGGER.addHandler(console_handler)
# LOGGER.addHandler(cw_handler)
# LOGGER.info("I hope you get this log, CloudWatch!")

# frontend = os.getenv('FRONTEND_URL') if os.getenv('FRONTEND_URL') is not None else "*"
# backend = os.getenv('BACKEND_URL') if os.getenv('BACKEND_URL') is not None else "*"
frontend = "*"
backend = "*"
# origins = [frontend, backend]
origins = "*"
print(origins)
cors = CORS(
  app, 
  resources={r"*": {"origins": origins}},
  expose_headers="location,link",
  allow_headers="content-type,if-modified-since,accept,authorization",
  methods="OPTIONS,GET,HEAD,POST"
)

@app.route("/", methods=['GET'])
def root_page():
  return "Hello World!"

@app.route("/api/message_groups", methods=['GET'])
@cross_origin()
def data_message_groups():
  user_sub = jwt_verifier.extract_cognito_user_id(request)
  if user_sub is not None: 
    model = MessageGroups.run(user_sub)
    return model['data'], 200
  else:
    return "You need to be authenticated", 401
  
    
@app.route("/api/messages/@<string:group_uuid>", methods=['GET'])
@cross_origin()
def data_messages(group_uuid):
  user_sub = jwt_verifier.extract_cognito_user_id(request)
  if user_sub is not None:
    model = Messages.run(user_sub, group_uuid)
    if model['errors'] is not None:
      return model['errors'], 422
    else:
      return model['data'], 200
  else:
    return "You need to be authenticated", 401

@app.route("/api/messages", methods=['POST','OPTIONS'])
@cross_origin()
def data_create_message():
  user_sender_handle = 'andrewbrown'
  user_receiver_handle = request.json['user_receiver_handle']
  message = request.json['message']

  model = CreateMessage.run(message=message,user_sender_handle=user_sender_handle,user_receiver_handle=user_receiver_handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route("/api/activities/home", methods=['GET'])
@cross_origin()
def data_home():
  authenticated = jwt_verifier.extract_cognito_user_id(request)
  model = HomeActivities.run()
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route("/api/activities/@<string:handle>", methods=['GET'])
@cross_origin()
def data_handle(handle):
  model = UserActivities.run(handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route("/api/activities/search", methods=['GET'])
@cross_origin()
def data_search():
  term = request.args.get('term')
  model = SearchActivities.run(term)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200


@app.route("/api/activities/notifications", methods=['GET'])
@cross_origin()
@xray_recorder.capture('activities_show_segment')
def data_notifications():
  data = NotificationsActivities.run()
  return data, 200

@app.route("/api/activities", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities():
  model = CreateActivity.run(request)
  if model['errors'] is not None:
    return model['errors']['message'], model['errors']['status']
  else:
    return model['data'], 200

@app.route("/api/activities/<string:activity_uuid>", methods=['GET'])
def data_show_activity(activity_uuid):
  data = ShowActivity.run(activity_uuid=activity_uuid)
  return data, 200

@app.route("/api/activities/<string:activity_uuid>/reply", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities_reply(activity_uuid):
  user_handle  = 'andrewbrown'
  message = request.json['message']
  model = CreateReply.run(message, user_handle, activity_uuid)
  if model['errors'] is not None:
    return "smthing went wrong", 422
  else:
    return model['data'], 200

if __name__ == "__main__":
  app.run(debug=True)