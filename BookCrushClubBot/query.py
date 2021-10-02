class Query:

    ADD_FICTION_BOOK = "INSERT INTO fiction_books VALUES(%s, %s, %s, %s, %s, %s);"

    ADD_NONFICTION_BOOK = "INSERT INTO nonfiction_books VALUES(%s, %s, %s, %s, %s, %s);"

    ADD_SHORT_STORY = "INSERT INTO short_stories VALUES(%s, %s, %s, %s, %s, %s);"

    CLEAR_FICTION_BOOKS = "DELETE FROM fiction_books;"

    CLEAR_NONFICTION_BOOKS = "DELETE FROM nonfiction_books;"

    CLEAR_SHORT_STORIES = "DELETE FROM short_stories;"

    GET_FICTION_BOOKS = (
        "SELECT book_name, authors FROM fiction_books WHERE user_id = %s;"
    )

    GET_FICTION_BOOKS_ALL = (
        "SELECT book_name, authors, ARRAY_AGG(display_name) "
        "FROM fiction_books GROUP BY book_name, authors;"
    )

    GET_NONFICTION_BOOKS = (
        "SELECT book_name, authors FROM nonfiction_books WHERE user_id = %s;"
    )

    GET_NONFICTION_BOOKS_ALL = (
        "SELECT book_name, authors, ARRAY_AGG(display_name) "
        "FROM nonfiction_books GROUP BY book_name, authors;"
    )

    GET_SHORT_STORIES = (
        "SELECT story_name, authors FROM short_stories WHERE user_id = %s;"
    )

    GET_SHORT_STORIES_ALL = (
        "SELECT story_name, authors, ARRAY_AGG(display_name) "
        "FROM short_stories GROUP BY story_name, authors "
        "ORDER BY RANDOM();"
    )

    GET_USERS = (
        "SELECT user_id FROM fiction_books "
        "UNION "
        "SELECT user_id FROM nonfiction_books "
        "UNION "
        "SELECT user_id FROM short_stories;"
    )

    REMOVE_FICTION_BOOK = (
        "DELETE FROM fiction_books WHERE user_id = %s AND book_name = %s;"
    )

    REMOVE_NONFICTION_BOOK = (
        "DELETE FROM nonfiction_books WHERE user_id = %s AND book_name = %s;"
    )

    REMOVE_SHORT_STORY = (
        "DELETE FROM short_stories WHERE user_id = %s AND story_name = %s;"
    )
