#!/usr/bin/env python3
import boto3
import os

def get_users():
    client = boto3.client('cognito-idp')
    params = {
        'UserPoolId': os.getenv("COGNITO_USER_POOLS_ID") or os.getenv("REACT_APP_AWS_USER_POOLS_ID"),
        'AttributesToGet': [
            'sub', 
            'email',
            'nickname',
            'name'
        ]
    }

    response = client.list_users(**params)
    users = response['Users']

    # print(json.dumps(users, sort_keys=True, indent=2, default=str))

    json_users = []

    for user in users:
        attrs = user['Attributes']
        json_user = {}
        for attr in attrs:
            json_user[attr['Name']] = attr['Value']
        json_users.append(json_user)

    return json_users