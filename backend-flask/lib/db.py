from psycopg_pool import ConnectionPool
import os
import re
import sys
from flask import current_app as app

class Db:
    @staticmethod
    def query_wrap_object(sql_query):
        wrapped_sql_query = f"""
        (SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
        {sql_query}
        ) object_row);
        """
        return wrapped_sql_query

    @staticmethod
    def query_wrap_array(sql_query):
        wrapped_sql_query = f"""
        (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json) FROM (
        {sql_query}
        ) array_row);
        """
        return wrapped_sql_query
    
    @staticmethod
    def load_sql_script(*args):
        script_path = os.path.join(app.root_path, 'db', 'sql', *args)
        with open(script_path, 'r') as f:
            template_content = f.read()
            return template_content

    def __init__(self, connection_url):
        ## can config pool size here as well
        ## self.pool = ConnectionPool(connection_url, min_size=1, max_size=5)
        self.pool = ConnectionPool(connection_url)

    def query_array_json(self,sql,params={}):
        wrapped_sql = self.query_wrap_array(sql)
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(wrapped_sql,params)
                json = cur.fetchone()
                #  ([],)
                return json[0]

    def query_object_json(self,sql,params={}):
        wrapped_sql = Db.query_wrap_object(sql)
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(wrapped_sql,params)
                json = cur.fetchone()
                print(json)
                if json == None:
                    return None
                else:
                    return json[0]

    def sql_query(self, sql, params={}):
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql,params)
                try:
                    json = cur.fetchone()
                    if json == None:
                        return None
                    else:
                        return json[0]
                except Exception:
                    return None


if os.getenv("FLASK_ENV") == "development":
    url_string = os.getenv("LOCAL_CONNECTION_URL")
else:
    url_string = os.getenv("RDS_CONNECTION_URL")

## when trying to run loccaly
if url_string == None:
    url_string = "postgresql://postgres:password@localhost:5432/cruddur" ## localhost environment 

db = Db(url_string)