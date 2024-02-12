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

    CLUBBOT_BOOK_EXISTS = (
        "SELECT EXISTS (SELECT 1 FROM books WHERE bname = %(name)s AND author = %(desc)s);"
    )

    POLLBOT_LINKED_POLL = (
        "SELECT name FROM poll WHERE id = %(id)s;"
    )

    POLLBOT_SYNC_POLL = (
        "INSERT INTO option (poll_id, index, name, is_date, description) "
        "SELECT %(id)s, %(index)s, %(name)s, 'f', %(desc)s "
        "WHERE NOT EXISTS (SELECT name,poll_id FROM option WHERE name = %(name)s AND poll_id = %(id)s) RETURNING TRUE;"
    )

    POLLBOT_MAX_INDEX = (
        "SELECT MAX(index) "
        "FROM option "
        "WHERE poll_id = %(id)s;"
    )

    POLLBOT_REMOVE_OPTION = (
        "DELETE FROM option "
        "WHERE poll_id = %(id)s AND name = %(name)s "
        "AND description = %(desc)s RETURNING TRUE;"
    )

    POLLBOT_BOOK_EXISTS = (
        "SELECT EXISTS (SELECT 1 FROM option WHERE poll_id = %(id)s AND name = %(name)s AND description = %(desc)s);"
    )

    POLLBOT_GET_OPTIONS = (
        "SELECT name,description "
        "FROM option "
        "WHERE poll_id = %(id)s;"
    )
