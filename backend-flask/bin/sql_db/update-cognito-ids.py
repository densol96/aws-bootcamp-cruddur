#!/usr/bin/env python3
import boto3
import os
import sys

current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, '..', '..'))
sys.path.append(parent_path)
from lib.db import db
from bin.cognito.helpers.get_users import get_users


def update_users_with_cognito_user_id(nickname, sub):
  sql = """
        UPDATE public.users
        SET cognito_user_id = %(sub)s
        WHERE
        nickname = %(nickname)s;
        """
  db.sql_query(sql, {
    'nickname' : nickname,
    'sub' : sub
  })

users = get_users()

for user in users:
    update_users_with_cognito_user_id(
        nickname=user['nickname'],
        sub=user['sub']
    )