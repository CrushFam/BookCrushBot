"""Constants of primary data type."""
from telegram.constants import CallbackQueryLimit, UpdateType

from .key import Key
from .message import Message


class Literal:
    """Constants of primary data type."""

    ADMINS_CHAT_ID = -1001407344499

    BROADCAST_INTERVAL = 2

    KEYS = [key.value for key in Key]

    MAX_BOOK_NAME = (
        CallbackQueryLimit.ANSWER_CALLBACK_QUERY_TEXT_LENGTH
        - max(len(Message.SUGGESTED_BOOK), len(Message.REMOVED_BOOK))
        - 6
    )  # 6 for {NAME}

    MAX_AUTHOR_NAME = MAX_BOOK_NAME

    SECTIONS = {"botm": "BOTM", "shortstory": "Short Story"}

    OPEN_LIBRARY_PARAMS = {
        "q": "QUERY",
    }

    OPEN_LIBRARY_URL = "https://openlibrary.org/search.json"

    UPDATES = [UpdateType.CALLBACK_QUERY, UpdateType.MESSAGE]

    LINKED_POLL = 7
