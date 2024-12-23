import boto3
import sys
from datetime import datetime, timedelta, timezone
import uuid
import os
import botocore.exceptions

class DynamoDb:
    def __init__(self, endpoint_url, table_name):
        self.endpoint_url = endpoint_url
        self.table_name = table_name

    def get_client(self):
        return boto3.client("dynamodb", endpoint_url = self.endpoint_url)
        
    def list_message_groups(self, user_id):
        query_params = {
            'TableName': self.table_name,
            'KeyConditionExpression': 'pk = :pk', #### AND ..... OR .......
            'ScanIndexForward': False,
            'Limit': 20,
            'ExpressionAttributeValues': {
                ':pk': {'S': f"GRP#{user_id}"}
            }
        }
        response = self.get_client().query(**query_params)
        items = response['Items']
        results = []
        for item in items:
            last_sent_at = item['sk']['S']
            results.append({
                'uuid': item['message_group_uuid']['S'],
                'user_name': item['user_name']['S'],
                'user_nickname': item['user_nickname']['S'],
                'message': item['message']['S'],
                'created_at': last_sent_at
            })
        return results
    
    def list_messages_in_chat(self, message_group_uuid):
        query_params = {
            'TableName': self.table_name,
            'KeyConditionExpression': 'pk = :pk',
            'ScanIndexForward': False,
            'Limit': 20,
            'ExpressionAttributeValues': {
                ':pk': {'S': f"MSG#{message_group_uuid}"}
            }
        }

        response = self.get_client().query(**query_params)
        items = response['Items']
        items.reverse()
        results = []
        print(items)
        for item in items:
            results.append({
                'uuid': item['message_uuid']['S'],
                'user_name': item['user_name']['S'],
                'user_nickname': item['user_nickname']['S'],
                'message': item['message']['S'],
                'created_at': item['sk']['S']
            })
        return results

    def create_message(self, message_group_uuid, message, my_user_uuid, my_user_display_name, my_user_handle):
        created_at = datetime.now().isoformat()
        message_uuid = str(uuid.uuid4())

        record = {
            'pk':   {'S': f"MSG#{message_group_uuid}"},
            'sk':   {'S': created_at },
            'message': {'S': message},
            'message_uuid': {'S': message_uuid},
            'user_uuid': {'S': my_user_uuid},
            'user_name': {'S': my_user_display_name},
            'user_nickname': {'S': my_user_handle}
        }
        # insert the record into the table
        result = self.get_client().put_item(
            TableName=self.table_name,
            Item=record
        )
        print("RESPONSE FROM add message boto3:dynamodb: ", result)

        return {
            'message_group_uuid': message_group_uuid,
            'uuid': my_user_uuid,
            'user_name': my_user_display_name,
            'user_nickname':  my_user_handle,
            'message': message,
            'created_at': created_at
        }
    
    def create_message_group(self, message,my_user_uuid, my_user_display_name, my_user_handle, other_user_uuid, other_user_display_name, other_user_handle):
        message_group_uuid = str(uuid.uuid4())
        message_uuid = str(uuid.uuid4())
        now = datetime.now(timezone.utc).astimezone().isoformat()
        last_message_at = now
        created_at = now

        my_message_group = {
            'pk': {'S': f"GRP#{my_user_uuid}"},
            'sk': {'S': last_message_at},
            'message_group_uuid': {'S': message_group_uuid},
            'message': {'S': message},
            'user_uuid': {'S': other_user_uuid},
            'user_name': {'S': other_user_display_name},
            'user_nickname':  {'S': other_user_handle}
        }

        other_message_group = {
            'pk': {'S': f"GRP#{other_user_uuid}"},
            'sk': {'S': last_message_at},
            'message_group_uuid': {'S': message_group_uuid},
            'message': {'S': message},
            'user_uuid': {'S': my_user_uuid},
            'user_name': {'S': my_user_display_name},
            'user_nickname':  {'S': my_user_handle}
        }

        message = {
            'pk':   {'S': f"MSG#{message_group_uuid}"},
            'sk':   {'S': created_at },
            'message': {'S': message},
            'message_uuid': {'S': message_uuid},
            'user_uuid': {'S': my_user_uuid},
            'user_name': {'S': my_user_display_name},
            'user_nickname': {'S': my_user_handle}
        }

        items = {
            self.table_name : [
                {'PutRequest': {'Item': my_message_group}},
                {'PutRequest': {'Item': other_message_group}},
                {'PutRequest': {'Item': message}}
            ]
        }
        print("I AM HERE")
        try:
            # Begin the transaction
            result = self.get_client().batch_write_item(RequestItems=items)
            print("RESPONSE FROM create group boto3:dynamodb: ", result)
            return {
                'message_group_uuid': message_group_uuid
            }
        except botocore.exceptions.ClientError as e:
            print('== create_message_group.error')
            print(e)
        except Exception as e:
            print("Unexpected error")
            print(e)


ddb = DynamoDb("http://dynamodb-local:8000", "cruddur-messages")
