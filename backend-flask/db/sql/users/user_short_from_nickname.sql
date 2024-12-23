SELECT
  users.uuid,
  users.nickname,
  users.name
FROM public.users
WHERE 
  users.nickname = %(nickname)s