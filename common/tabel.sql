CREATE TABLE auto_quiz(
  id SERIAL,
  name VARCHAR(256) UNIQUE,
  hashed_password VARCHAR(256),
  salt VARCHAR(256),
  point INT
);