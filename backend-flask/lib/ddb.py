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
                'display_name': item['user_display_name']['S'],
                'handle': item['user_handle']['S'],
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
        for item in items:
            results.append({
                'uuid': item['message_uuid']['S'],
                'display_name': item['user_display_name']['S'],
                'handle': item['user_handle']['S'],
                'message': item['message']['S'],
                'created_at': item['sk']['S']
            })
        return results

ddb = DynamoDb("http://dynamodb-local:8000", "cruddur-messages")
