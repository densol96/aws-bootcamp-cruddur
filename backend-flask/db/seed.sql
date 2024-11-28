-- INSERT INTO public.users (name, nickname, email, cognito_user_id)
-- VALUES
--   ('Andrew Brown', 'andrewbrown', 'test@mail.com' ,'MOCK'),
--   ('Andrew Bayko', 'bayko', 'test2@mail.com','MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.nickname = 'andrewbrown' LIMIT 1),
    'dq;knmdw;qklmklqwdl;kqwmdklqwmdl;kqmkmqwd',
    current_timestamp + interval '10 day'
  ),
   (
    (SELECT uuid from public.users WHERE users.nickname = 'bayko' LIMIT 1),
    'More text hahahhahahhahahha!',
    current_timestamp + interval '10 day'
  ),
  (
    (SELECT uuid from public.users WHERE users.nickname = 'bayko' LIMIT 1),
    'Some More text hahahhahahhahahha!',
    current_timestamp + interval '10 day'
  )
  ;