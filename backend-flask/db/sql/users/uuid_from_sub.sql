SELECT
    uuid
FROM
    public.users
WHERE
    cognito_user_id = %(cognito_user_id)s;