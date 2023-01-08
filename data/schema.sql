-- Set up the tables.
\connect bcc
DROP TABLE IF EXISTS keyvalue;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS users;

CREATE TABLE users(
       user_id BIGINT PRIMARY KEY,
       full_name TEXT
);


CREATE TABLE books(
       user_id BIGINT REFERENCES users ON DELETE CASCADE,
       sect TEXT,
       bname TEXT,
       author TEXT,
       PRIMARY KEY (user_id, sect, bname, author)
);

CREATE TABLE keyvalue(
       keytxt TEXT PRIMARY KEY,
       valuetxt TEXT
);

INSERT INTO keyvalue VALUES
       ('genrebotm', 'Any Genre'),
       ('genreshortstory', 'Any Genre'),
       ('maxsuggestionsbotm', '2'),
       ('maxsuggestionsshortstory', '2'),
       ('starttext', 'Hey there FULL_NAME!');
