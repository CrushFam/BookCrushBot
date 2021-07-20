from telegram.ext import Filters, CallbackQueryHandler, CommandHandler, MessageHandler
from .choose import suggest_by_isbn, suggest_by_name, suggest_raw
from .session import (
    start,
    remove,
    remove_book,
    suggest,
    suggest_book,
)
from .base import (
    get_fiction,
    get_nonfiction,
    redirect_update,
    send_help,
    send_start,
    start_fiction,
    start_nonfiction,
    start_short_story,
    stay_awake_ping,
)


handlers = {
    CallbackQueryHandler: [
        ({"callback": start, "pattern": "^start$"}, ()),
        ({"callback": suggest, "pattern": "^suggest$"}, ()),
        ({"callback": suggest_book, "pattern": r"^suggest_[\d]+$"}, ()),
        ({"callback": remove, "pattern": "^remove$"}, ()),
        ({"callback": remove_book, "pattern": r"^remove_[\d]+$"}, ()),
        ({"callback": suggest_by_isbn, "pattern": "^isbn$"}, ()),
        ({"callback": suggest_by_name, "pattern": "^name$"}, ()),
        ({"callback": suggest_raw, "pattern": "^raw$"}, ()),
    ],
    CommandHandler: [
        ({"command": "fiction", "callback": start_fiction}, ()),
        ({"command": "getfiction", "callback": get_fiction}, ()),
        ({"command": "getnonfiction", "callback": get_nonfiction}, ()),
        ({"command": "help", "callback": send_help}, ()),
        ({"command": "nonfiction", "callback": start_nonfiction}, ()),
        ({"command": "shortstory", "callback": start_short_story}, ()),
        ({"command": "start", "callback": send_start}, ()),
    ],
    MessageHandler: [
        ({"filters": Filters.chat_type.channel, "callback": stay_awake_ping}, ()),
        ({"filters": Filters.text, "callback": redirect_update}, ()),
    ],
}
