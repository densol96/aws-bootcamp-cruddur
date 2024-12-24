import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource(
 'dynamodb',
 region_name='eu-north-1',
 endpoint_url="http://dynamodb.eu-north-1.amazonaws.com"
)


def lambda_handler(event, context):
  print("===============================================================")
  print("===============================================================")
  print("===============================================================")
  print('event-data',event)
  eventName = event['Records'][0]['eventName']
  if (eventName == 'REMOVE'):
    print("skip REMOVE event")
    return
  pk = event['Records'][0]['dynamodb']['Keys']['pk']['S']
  sk = event['Records'][0]['dynamodb']['Keys']['sk']['S']
  if pk.startswith('MSG#'):
    group_uuid = pk.replace("MSG#","")
    message = event['Records'][0]['dynamodb']['NewImage']['message']['S']
    print("GRUP ===>",group_uuid,message)
    
    table_name = 'cruddur-messages'
    index_name = 'message-group-sk-index'
    table = dynamodb.Table(table_name)
    data = table.query(
      IndexName=index_name,
      KeyConditionExpression=Key('message_group_uuid').eq(group_uuid)
    )
    print("AFFECTED MESSAGE GROUPS: ===>", data['Items'])
    
    # recreate the message group rows with new SK value
    for i in data['Items']:
      old_updated_grp = table.delete_item(Key={'pk': i['pk'], 'sk': i['sk']})
      print("DELETE(old_updated_grp) ===>", old_updated_grp)
      
      new_updated_grp = table.put_item(
        Item={
          'pk': i['pk'],
          'sk': sk,
          'message_group_uuid':i['message_group_uuid'],
          'message':message,
          'user_name': i['user_name'],
          'user_nickname': i['user_nickname'],
          'user_uuid': i['user_uuid']
        }
      )
      print("CREATE(new_updated_grp) ===>", new_updated_grp)
  print("===============================================================")
  print("===============================================================")
  print("===============================================================")
