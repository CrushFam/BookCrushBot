class Query:

    ADD_FICTION_BOOK = "INSERT INTO fiction_books VALUES(%s, %s, %s, %s, %s, %s);"

    ADD_NONFICTION_BOOK = "INSERT INTO nonfiction_books VALUES(%s, %s, %s, %s, %s, %s);"

    GET_FICTION_BOOKS = (
        "SELECT book_name, authors FROM fiction_books WHERE user_id = %s;"
    )

    GET_FICTION_BOOKS_ALL = (
        "SELECT display_name, book_name, authors FROM fiction_books;"
    )

    GET_NONFICTION_BOOKS = (
        "SELECT book_name, authors FROM nonfiction_books WHERE user_id = %s;"
    )

    GET_NONFICTION_BOOKS_ALL = (
        "SELECT display_name, book_name, authors FROM nonfiction_books;"
    )

    REMOVE_FICTION_BOOK = (
        "DELETE FROM fiction_books WHERE user_id = %s AND book_name = %s;"
    )

    REMOVE_NONFICTION_BOOK = (
        "DELETE FROM nonfiction_books WHERE user_id = %s AND book_name = %s;"
    )
