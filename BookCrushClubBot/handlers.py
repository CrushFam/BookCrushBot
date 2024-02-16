"""Handlers for updates."""

from telegram.ext import (CallbackQueryHandler, CommandHandler, MessageHandler,
                          filters)

from BookCrushClubBot.base.callback_query import (action_remove,
                                                  action_suggest,
                                                  choose_action,
                                                  confirm_remove,
                                                  confirm_suggest)
from BookCrushClubBot.base.command import (books, broadcast, clear, get, help_,
                                           list_, set_, start, mkposts, getbookinfo, poll, sync_poll, days_since, haikudetect, get_random_quote, forward_offtopic)
from BookCrushClubBot.base.message import fallback, handle_text
from BookCrushClubBot.constants import CallbackData, Literal
from BookCrushClubBot.utils.misc import schedule_jobs


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
        _cmd(mkposts, "mkposts", filters.Chat(Literal.ADMINS_CHAT_ID)),
        _cmd(getbookinfo, "getbookinfo", filters.Chat(Literal.ADMINS_CHAT_ID)),
        _cmd(set_, "set", filters.Chat(Literal.ADMINS_CHAT_ID)),
        _cmd(poll, "poll", None),
        _cmd(sync_poll, "sync", None),
        _cmd(start, "start", None),
        _cmd(books, "books", None),
        _cmd(get_random_quote, "quote", None),
        _cmd(schedule_jobs, "schedule", filters.ChatType.PRIVATE),
        _cmd(forward_offtopic, "ot", filters.Chat(Literal.BOOKCRUSHCLUB_CHAT_ID) & filters.User(Literal.OT_ADMINS_IDS)),
    ],
    MessageHandler: [
        _msg(days_since, filters.Regex(r'(?i)a little life') & (filters.Chat(Literal.ADMINS_CHAT_ID) | filters.Chat(Literal.BOOKCRUSHCLUB_CHAT_ID))),
        _msg(haikudetect, filters.Text() & (filters.Chat(Literal.BOOKCRUSHCLUB_CHAT_ID) | filters.Chat(Literal.ADMINS_CHAT_ID))),
        _msg(handle_text, filters.ChatType.PRIVATE & ~filters.COMMAND),
        _msg(fallback, filters.ChatType.PRIVATE),
    ],
}
