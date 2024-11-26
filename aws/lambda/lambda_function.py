import json
import psycopg2
import os

def lambda_handler(event, context):
    user = event['request']['userAttributes']
    conn = None

    try:
        conn = psycopg2.connect(
            os.getenv("PROD_CONNECTION_URL")
        )
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (name, nickname, email, cognito_user_id) VALUES(%s, %s, %s, %s)",
            (user['name'], user['nickname'], user['email'], user['sub'])
        )
        conn.commit() 

    except (Exception, psycopg2.DatabaseError) as error:
        print("Handled error => ", error)
        
    finally:
        if conn is not None:
            cur.close()
            conn.close()
            print('Database connection closed.')

    return event