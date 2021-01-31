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
    redirect_update,
    send_help,
    send_start,
    start_fiction,
    start_nonfiction,
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
        ({"command": "help", "callback": send_help}, ()),
        ({"command": "nonfiction", "callback": start_nonfiction}, ()),
        ({"command": "start", "callback": send_start}, ()),
    ],
    MessageHandler: [({"filters": Filters.text, "callback": redirect_update}, ())],
}
