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
        authors: list,
        genres: list,
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
        authors: list,
        genres: list,
        notes: str,
    ):

        cursor = self.connection.cursor()
        cursor.execute(
            Query.ADD_NONFICTION_BOOK,
            (user_id, display_name, book_name, authors, genres, notes),
        )
        self.connection.commit()
        cursor.close()

    def add_short_story(
        self,
        user_id: int,
        display_name: str,
        story_name: str,
        authors: list,
        genres: list,
        notes: str,
    ):

        cursor = self.connection.cursor()
        cursor.execute(
            Query.ADD_SHORT_STORY,
            (user_id, display_name, story_name, authors, genres, notes),
        )
        self.connection.commit()
        cursor.close()

    def get_fiction_books(self, user_id: int):

        cursor = self.connection.cursor()
        cursor.execute(Query.GET_FICTION_BOOKS, (user_id,))
        yield from cursor
        cursor.close()

    def get_fiction_books_all(self):

        cursor = self.connection.cursor()
        cursor.execute(Query.GET_FICTION_BOOKS_ALL)
        yield from cursor
        cursor.close()

    def get_nonfiction_books(self, user_id: int):

        cursor = self.connection.cursor()
        cursor.execute(Query.GET_NONFICTION_BOOKS, (user_id,))
        yield from cursor
        cursor.close()

    def get_nonfiction_books_all(self):

        cursor = self.connection.cursor()
        cursor.execute(Query.GET_NONFICTION_BOOKS_ALL)
        yield from cursor
        cursor.close()

    def get_short_stories(self, user_id: int):

        cursor = self.connection.cursor()
        cursor.execute(Query.GET_SHORT_STORIES, (user_id,))
        yield from cursor
        cursor.close()

    def get_short_stories_all(self):

        cursor = self.connection.cursor()
        cursor.execute(Query.GET_SHORT_STORIES_ALL)
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

    def remove_short_story(self, user_id: int, story_name: str):

        cursor = self.connection.cursor()
        cursor.execute(Query.REMOVE_SHORT_STORY, (user_id, story_name))
        self.connection.commit()
        cursor.close()
