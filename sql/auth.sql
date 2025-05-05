-- ALTER TABLE Employee
-- ADD COLUMN role_login VARCHAR(50) UNIQUE,
-- ADD COLUMN password_hash TEXT;

UPDATE Employee
SET role_login = 'manager', password_hash = '0de63af4ba4fbdc07aa9885bbd55628f35f4c202f727c9d0b3e03205ac919769'
WHERE id_employee = 'emp001';

UPDATE Employee
SET role_login = 'cashier1', password_hash = 'c74d954f8864769137b23b1d2055fcb21c5d9d1dea1d6cbf9ed0bc638aa8f439'
WHERE id_employee = 'emp003';

UPDATE Employee
SET role_login = 'cashier2', password_hash = '9b07ea519f163aed2a6d58c6c8042eb0d5f1c3b991ba1069f467ed2015fc42e7'
WHERE id_employee = 'emp004';

UPDATE Employee
SET role_login = 'cashier3', password_hash = '04d68de25a006b2ef59e5c48568cf1d7b599e6486f275ee627984fac488cd3aa'
WHERE id_employee = 'emp005';

UPDATE Employee
SET role_login = 'cashier4', password_hash = 'fe1a1b24a201f228244333fbd397ecdb99a7cc7c98e387eedbaaaa21190bc18e'
WHERE id_employee = 'emp006';