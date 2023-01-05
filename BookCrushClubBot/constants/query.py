"""Queries for database information."""


class Query:
    """Queries for database information."""

    ADD_BOOK = (
        "INSERT INTO books "
        "VALUES (%(user_id)s, %(section)s, %(name)s, %(author)s) "
        "ON CONFLICT (user_id, sect, bname, author) DO NOTHING "
        "RETURNING TRUE;"
    )

    ADD_USER = (
        "INSERT INTO users VALUES (%(user_id)s, %(full_name)s) "
        "ON CONFLICT (user_id) DO UPDATE SET full_name = %(full_name)s;"
    )

    CLEAR_SECTION = "DELETE FROM books WHERE sect = %(section)s;"

    GET_BOOKS = (
        "SELECT bname, author FROM books "
        "WHERE user_id = %(user_id)s AND sect = %(section)s;"
    )

    GET_USERS = "SELECT user_id FROM users;"

    GET_VALUE = "SELECT valuetxt FROM keyvalue WHERE keytxt = %(key)s;"

    LIST_SECTION = (
        "SELECT b.bname, b.author, ARRAY_AGG(u.full_name) "
        "FROM books b INNER JOIN users u ON u.user_id = b.user_id "
        "WHERE sect = %(section)s GROUP BY b.bname, b.author "
        "ORDER BY RANDOM();"
    )

    REMOVE_BOOK = (
        "DELETE FROM books "
        "WHERE user_id = %(user_id)s AND sect = %(section)s "
        "AND bname = %(name)s AND author = %(author)s RETURNING TRUE;"
    )

    SET_VALUE = (
        "UPDATE keyvalue SET valuetxt = %(value)s "
        "WHERE keytxt = %(key)s RETURNING TRUE;"
    )
