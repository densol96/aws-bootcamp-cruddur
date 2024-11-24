import json
import psycopg2
import os

def lambda_handler(event, context):
    user = event['request']['userAttributes']
    print(user) # {'sub': '20fc191c-20c...', 'email_verified': 'true', 'cognito:user_status': 'CONFIRMED', 'nickname': 'solodeni', 'name': 'Deniss', 'email': 'deniss11sol@gmail.com'}
    # try:
    #     conn = psycopg2.connect(
    #         host=(os.getenv('PG_HOSTNAME')),
    #         database=(os.getenv('PG_DATABASE')),
    #         user=(os.getenv('PG_USERNAME')),
    #         password=(os.getenv('PG_SECRET'))
    #     )
    #     cur = conn.cursor()
    #     cur.execute("INSERT INTO users (display_name, handle, cognito_user_id) VALUES(%s, %s, %s)", (user['name'], user['email'], user['sub']))
    #     conn.commit() 

    # except (Exception, psycopg2.DatabaseError) as error:
    #     print(error)
        
    # finally:
    #     if conn is not None:
    #         cur.close()
    #         conn.close()
    #         print('Database connection closed.')

    return event