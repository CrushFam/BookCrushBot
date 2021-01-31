import psycopg2
from .query import Query


class Database:
    def __init__(self, database_url: str):

        self.connection = psycopg2.connect(database_url)

    def __del__(self):

        self.connection.close()

    def add_fiction_book(
        self,
        user_id: int,
        display_name: str,
        book_name: str,
        authors: str,
        genres: str,
        notes: str,
    ):

        cursor = self.connection.cursor()
        cursor.execute(
            Query.ADD_FICTION_BOOK,
            (user_id, display_name, book_name, authors, genres, notes),
        )
        self.connection.commit()
        cursor.close()

    def add_nonfiction_book(
        self,
        user_id: int,
        display_name: str,
        book_name: str,
        authors: str,
        genres: str,
        notes: str,
    ):

        cursor = self.connection.cursor()
        cursor.execute(
            Query.ADD_NONFICTION_BOOK,
            (user_id, display_name, book_name, authors, genres, notes),
        )
        self.connection.commit()
        cursor.close()

    def get_fiction_books(self, user_id: int):

        cursor = self.connection.cursor()
        cursor.execute(Query.GET_FICTION_BOOKS, (user_id,))
        yield from cursor
        cursor.close()

    def get_nonfiction_books(self, user_id: int):

        cursor = self.connection.cursor()
        cursor.execute(Query.GET_NONFICTION_BOOKS, (user_id,))
        yield from cursor
        cursor.close()

    def remove_fiction_book(self, user_id: int, book_name: str):

        cursor = self.connection.cursor()
        cursor.execute(Query.REMOVE_FICTION_BOOK, (user_id, book_name))
        self.connection.commit()
        cursor.close()

    def remove_nonfiction_book(self, user_id: int, book_name: str):

        cursor = self.connection.cursor()
        cursor.execute(Query.REMOVE_NONFICTION_BOOK, (user_id, book_name))
        self.connection.commit()
        cursor.close()
