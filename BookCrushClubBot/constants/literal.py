"""Constants of primary data type."""

from telegram.constants import (MAX_ANSWER_CALLBACK_QUERY_TEXT_LENGTH,
                                UPDATE_CALLBACK_QUERY, UPDATE_MESSAGE)

from .key import Key
from .message import Message


class Literal:
    """Constants of primary data type."""

    ADMINS_CHAT_ID = -1001407344499

    BROADCAST_INTERVAL = 2

    KEYS = [key.value for key in Key]

    MAX_BOOK_NAME = (
        MAX_ANSWER_CALLBACK_QUERY_TEXT_LENGTH
        - max(len(Message.SUGGESTED_BOOK), len(Message.REMOVED_BOOK))
        - 6
    )  # 6 for {NAME}

    MAX_AUTHOR_NAME = MAX_BOOK_NAME

    SECTIONS = {"botm": "BOTM", "shortstory": "Short Story"}

    OPEN_LIBRARY_PARAMS = {
        "q": "QUERY",
        "author": "AUTHOR",
        "fields": "title, author_name",
        "limit": 5,
    }

    OPEN_LIBRARY_URL = "https://openlibrary.org/search.json"

    UPDATES = [UPDATE_CALLBACK_QUERY, UPDATE_MESSAGE]
