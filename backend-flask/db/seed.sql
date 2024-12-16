INSERT INTO public.users (name, nickname, email, cognito_user_id)
VALUES
  ('Deniss Solovjovs', 'solodeni', 'deniss11sol@gmail.com' ,'MOCK'),
  ('David Solovjovs', 'davidka', 'david2020sol@gmail.com','MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.nickname = 'solodeni' LIMIT 1),
    'Hello my friends',
    current_timestamp + interval '10 day'
  ),
   (
    (SELECT uuid from public.users WHERE users.nickname = 'davidka' LIMIT 1),
    'More text hahahhahahhahahha!',
    current_timestamp + interval '10 day'
  ),
  (
    (SELECT uuid from public.users WHERE users.nickname = 'davidka' LIMIT 1),
    'Some More text hahahhahahhahahha!',
    current_timestamp + interval '10 day'
  )
  ;