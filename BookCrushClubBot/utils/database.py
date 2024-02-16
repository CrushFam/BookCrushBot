"""Database for stoing information."""

import psycopg2

from BookCrushClubBot.constants import Query


class Database:
    """Database for storing information."""

    def __init__(self, database_url: str):
        """Create a new database connection with database URL."""
        self._connection = psycopg2.connect(database_url)

    def _failsafe(func):
        """Commit or rollback facility for queries."""

        def wrapped(self, *args, **kwargs):
            try:
                ret = func(self, *args, **kwargs)
            except psycopg2.Error as e:
                self._connection.rollback()
                raise e
            else:
                self._connection.commit()
                return ret

        return wrapped

    @_failsafe
    def add_book(self, user_id: int, section: str, name: str, author: str) -> bool:
        """Add the book to database."""
        cur = self._connection.cursor()
        cur.execute(
            Query.ADD_BOOK,
            {"user_id": user_id, "section": section, "name": name, "author": author},
        )
        row = cur.fetchone()
        ret = row[0] if row else False
        cur.close()
        return ret

    @_failsafe
    def add_user(self, user_id: int, full_name: str):
        """Add the user to database."""
        cur = self._connection.cursor()
        cur.execute(Query.ADD_USER, {"user_id": user_id, "full_name": full_name})
        cur.close()

    @_failsafe
    def clear_section(self, section: str):
        """Clear the books of a section."""
        cur = self._connection.cursor()
        cur.execute(Query.CLEAR_SECTION, {"section": section})
        cur.close()

    def get_books(self, user_id: int, section: str) -> list:
        """Get the books of the user."""
        cur = self._connection.cursor()
        cur.execute(Query.GET_BOOKS, {"user_id": user_id, "section": section})
        books = list(cur)
        cur.close()
        return books
    
    def get_authors(self) -> list:
        """Get the authors"""
        cur = self._connection.cursor()
        cur.execute(Query.GET_AUTHORS)
        authors = list(cur)
        cur.close()
        return authors

    def get_users(self) -> list:
        """Get the users in database."""
        cur = self._connection.cursor()
        cur.execute(Query.GET_USERS)
        users = [user_id for user_id, in cur]
        cur.close()
        return users

    def get_value(self, key: str) -> str:
        """Get the value of the key."""
        cur = self._connection.cursor()
        cur.execute(Query.GET_VALUE, {"key": key})
        row = cur.fetchone()
        value = row[0] if row else None
        cur.close()
        return value

    def list_section(self, section: str) -> list:
        """List the books of the section."""
        cur = self._connection.cursor()
        cur.execute(Query.LIST_SECTION, {"section": section})
        books = list(cur)
        cur.close()
        return books

    @_failsafe
    def remove_book(self, user_id: int, section: str, name: str, author: str) -> bool:
        """Remove the book from database."""
        cur = self._connection.cursor()
        cur.execute(
            Query.REMOVE_BOOK,
            {"user_id": user_id, "section": section, "name": name, "author": author},
        )
        row = cur.fetchone()
        ret = row[0] if row else False
        cur.close()
        return ret

    @_failsafe
    def set_value(self, key: str, value: str) -> bool:
        """Set the value of the key."""
        cur = self._connection.cursor()
        cur.execute(Query.SET_VALUE, {"key": key, "value": value})
        row = cur.fetchone()
        ret = row[0] if row else False
        return ret
    
    def get_poll(self, id: int) -> str:
        """Get linked poll details"""
        cur = self._connection.cursor()
        cur.execute(Query.POLLBOT_LINKED_POLL, {"id": id})
        row = cur.fetchone()
        ret = row[0] if row else False
        return ret
    
    @_failsafe
    def sync(self, id: int, index: int, name: str, desc: str) -> bool:
        """sync the poll bot with club bot suggestions"""
        cur = self._connection.cursor()
        cur.execute(Query.POLLBOT_SYNC_POLL, {"id": id, "index": index, "name": name, "desc": desc})
        row = cur.fetchone()
        ret = row[0] if row else False
        return ret
    
    def get_max_index (self, id: int) -> int:
        cur = self._connection.cursor()
        cur.execute(Query.POLLBOT_MAX_INDEX, {"id": id})
        row = cur.fetchone()
        ret = row[0] if row else 0
        return ret
    
    def book_exists (self, name: str, desc: str, id: int) -> bool:
        cur = self._connection.cursor()
        cur.execute(Query.POLLBOT_BOOK_EXISTS, {"name": name, "desc":desc, "id": id})
        row = cur.fetchone()
        ret = row[0] if row else False
        return ret
    
    def club_book_exists (self, name: str, desc: str) -> bool:
        cur = self._connection.cursor()
        cur.execute(Query.CLUBBOT_BOOK_EXISTS, {"name": name, "desc":desc})
        row = cur.fetchone()
        ret = row[0] if row else False
        return ret
    
    @_failsafe
    def remove_polloption (self, name: str, desc: str, id: int) -> bool:
        cur = self._connection.cursor()
        cur.execute(Query.POLLBOT_REMOVE_OPTION, {"name": name, "desc":desc, "id": id})
        row = cur.fetchone()
        ret = row[0] if row else 0
        return ret
    
    def get_options (self, id: int) -> list:
        cur = self._connection.cursor()
        cur.execute(Query.POLLBOT_GET_OPTIONS, {"id": id})
        options = list(cur)
        cur.close()
        return options
