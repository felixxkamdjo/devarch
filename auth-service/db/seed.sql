-- 

DELETE FROM users;

INSERT INTO users (email, user_firstname, user_lastname, role, password_hash, salt, created_at, updated_at) VALUES

  -- Admin
  ('admin@devarch.io',
   'Admin', 'DevArch',
   'admin',
   'HASH_PLACEHOLDER', 'SALT_PLACEHOLDER',
   '2025-01-01 00:00:00', '2025-01-01 00:00:00'),

  -- Auteurs
  ('felix@devarch.io',
   'Felix', 'Kamdjo',
   'author',
   'HASH_PLACEHOLDER', 'SALT_PLACEHOLDER',
   '2025-01-10 08:00:00', '2025-01-10 08:00:00'),

  ('amara@devarch.io',
   'Amara', 'Diallo',
   'author',
   'HASH_PLACEHOLDER', 'SALT_PLACEHOLDER',
   '2025-02-05 10:30:00', '2025-02-05 10:30:00'),

  ('chen@devarch.io',
   'Chen', 'Wei',
   'author',
   'HASH_PLACEHOLDER', 'SALT_PLACEHOLDER',
   '2025-03-12 14:15:00', '2025-03-12 14:15:00'),

  ('sara@devarch.io',
   'Sara', 'Mensah',
   'author',
   'HASH_PLACEHOLDER', 'SALT_PLACEHOLDER',
   '2025-04-01 09:00:00', '2025-04-01 09:00:00');
  -- Lecteurs
  ('usr-005',
   'Sara Mensah',
   'sara@devarch.io',
   '$2b$12$KIXtEbSB5KlZBhD0W2v8mO9GkFzLpQnRsYdTuVwXaAbCcDdEeFfG',
   'reader',
   '2025-04-01 09:00:00',
   '2025-04-01 09:00:00'),

  ('usr-006',
   'Lucas Ngoma',
   'lucas@devarch.io',
   '$2b$12$KIXtEbSB5KlZBhD0W2v8mO9GkFzLpQnRsYdTuVwXaAbCcDdEeFfG',
   'reader',
   '2025-04-15 11:45:00',
   '2025-04-15 11:45:00');