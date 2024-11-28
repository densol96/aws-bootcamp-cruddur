WITH inserted AS (
    INSERT INTO public.activities (user_uuid, message, expires_at)
    VALUES (
        (
            SELECT uuid 
            FROM public.users 
            WHERE users.cognito_user_id = %(cognito_user_id)s
            LIMIT 1
        ),
        %(message)s,
        %(expires_at)s
    )
    RETURNING *
),
complete_activity_data AS (
    SELECT
    inserted.uuid,
    users.name,
    users.nickname,
    inserted.message,
    inserted.replies_count,
    inserted.reposts_count,
    inserted.likes_count,
    inserted.reply_to_activity_uuid,
    inserted.expires_at,
    inserted.created_at
    FROM inserted
    JOIN users ON users.uuid = inserted.user_uuid
    LIMIT 1
) 
SELECT COALESCE(
    row_to_json(complete_activity_data), '{}'::json
) AS result
FROM complete_activity_data;
