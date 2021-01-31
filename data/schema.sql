CREATE TABLE fiction_books (
       user_id BIGINT,
       display_name TEXT,
       book_name TEXT,
       authors TEXT[] NOT NULL,
       genres TEXT[] NOT NULL,
       note TEXT,
       PRIMARY KEY (user_id, book_name)
);

CREATE TABLE nonfiction_books (
       user_id BIGINT,
       display_name TEXT,
       book_name TEXT,
       authors TEXT[] NOT NULL,
       genres TEXT[] NOT NULL,
       note TEXT,
       PRIMARY KEY (user_id, book_name)
);
