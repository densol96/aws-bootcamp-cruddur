from datetime import datetime, timedelta, timezone
from opentelemetry import trace
import time # testing duration_ms in honeycomb telemetry
from lib.db import db, Db

tracer = trace.get_tracer("playing-around")

green = '\033[92m'
no_color = '\033[0m'

class HomeActivities:
  @staticmethod
  def run():
    model = {
      'errors': None,
      'data': None
    }
    try:
      sql = Db.load_sql_script("activities", "select_all.sql")
      model['data'] = db.query_array_json(sql)
    except Exception as e:
      print(f'{green}----- services/home_activities.py {e} -----{no_color}')
      model['errors'] = "This service is currently unavailable."
    return model