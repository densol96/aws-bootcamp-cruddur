SELECT
  users.uuid,
  users.nickname,
  users.name
FROM public.users
WHERE 
  users.cognito_user_id = %(cognito_user_id)s