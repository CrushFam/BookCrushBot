"""Handlers for updates."""

from telegram.ext import (CallbackQueryHandler, CommandHandler, MessageHandler,
                          filters)

from BookCrushClubBot.base.callback_query import (action_remove,
                                                  action_suggest,
                                                  choose_action,
                                                  confirm_remove,
                                                  confirm_suggest)
from BookCrushClubBot.base.command import (books, broadcast, clear, get, help_,
                                           list_, set_, start)
from BookCrushClubBot.base.message import fallback, handle_text
from BookCrushClubBot.constants import CallbackData, Literal


def _cbq(callback, pattern):
    return {"callback": callback, "pattern": pattern}


def _cmd(callback, command, filters):
    return {"callback": callback, "command": command, "filters": filters}


def _msg(callback, filters):
    return {"callback": callback, "filters": filters}


handlers = {
    CallbackQueryHandler: [
        _cbq(action_remove, CallbackData.ACTION_REMOVE),
        _cbq(action_suggest, CallbackData.ACTION_SUGGEST),
        _cbq(choose_action, CallbackData.CHOOSE_ACTION.replace("{SECTION}", "+")),
        _cbq(books, CallbackData.CHOOSE_SECTION),
        _cbq(confirm_remove, CallbackData.CONFIRM_REMOVE.replace("{IX}", "+")),
        _cbq(confirm_suggest, CallbackData.CONFIRM_SUGGEST.replace("{IX}", "+")),
    ],
    CommandHandler: [
        _cmd(broadcast, "broadcast", filters.Chat(Literal.ADMINS_CHAT_ID)),
        _cmd(clear, "clear", filters.Chat(Literal.ADMINS_CHAT_ID)),
        _cmd(get, "get", filters.Chat(Literal.ADMINS_CHAT_ID)),
        _cmd(help_, "help", None),
        _cmd(list_, "list", filters.Chat(Literal.ADMINS_CHAT_ID)),
        _cmd(set_, "set", filters.Chat(Literal.ADMINS_CHAT_ID)),
        _cmd(start, "start", None),
        _cmd(books, "books", None),
    ],
    MessageHandler: [
        _msg(handle_text, filters.ChatType.PRIVATE & ~filters.COMMAND),
        _msg(fallback, filters.ChatType.PRIVATE),
    ],
}
