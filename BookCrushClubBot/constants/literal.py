"""Constants of primary data type."""
from telegram.constants import CallbackQueryLimit, UpdateType

from .key import Key
from .message import Message


class Literal:
    """Constants of primary data type."""

    ADMINS_CHAT_ID = -1001407344499

    BOOKCRUSHCLUB_CHAT_ID = -1001305978977

    OT_CHAT_ID = -1001442004442

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

    TIME_SINCE_A_LITTLE_LIFE = 0

    OT_ADMINS_IDS = [1194136014,967657040,15024063,998854724,441689112,515599610]