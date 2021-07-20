import logging
from telegram import Update
from telegram.ext import CallbackContext
from .constants import Constants
from .message import Message
from .session import start


def __get_items(session: str, update: Update, context: CallbackContext):

    if update.message.chat.id != Constants.ADMINS_GROUP:
        update.message.reply_text(text=Message.UNAUTHORIZED_COMMAND)
        return

    database = context.bot_data["database"]

    if session == Constants.FICTION_SESSION:
        genre = "Fiction"
        items = database.get_fiction_books_all()
    elif session == Constants.NONFICTION_SESSION:
        genre = "Non Fiction"
        items = database.get_nonfiction_books_all()
    elif session == Constants.SHORT_STORY_SESSION:
        genre = "Short Story"
        items = database.get_short_stories_all()

    ditems = {}
    count = 0
    for (name, book, authors) in items:
        ditems.setdefault((book, tuple(authors)), []).append(name)
        count += 1

    splits = [
        Message.BOOK_FULL.format(
            BOOK_NAME=book, AUTHORS=", ".join(authors), NAMES=", ".join(names)
        )
        for ((book, authors), names) in ditems.items()
    ]

    books = "\n".join(splits)
    text = Message.BOOKS_DISPLAY.format(
        GENRE=genre, BOOKS=books, REPEAT=count - len(ditems), TOTAL=count
    )
    update.message.reply_html(text)


def clear_previous_state(context: CallbackContext):

    msg = context.user_data.pop("baseMessage", None)
    if msg:
        msg.edit_reply_markup()
    context.user_data.clear()


def get_fiction(update: Update, context: CallbackContext):

    __get_items(Constants.FICTION_SESSION, update, context)


def get_nonfiction(update: Update, context: CallbackContext):

    __get_items(Constants.NONFICTION_SESSION, update, context)


def get_short_story(update: Update, context: CallbackContext):

    __get_items(Constants.SHORT_STORY_SESSION, update, context)


def redirect_update(update: Update, context: CallbackContext):

    if update.message.chat.type != update.message.chat.PRIVATE:
        return
    func = context.user_data.pop("redirectUpdate", None)
    if func:
        func(update, context)
    else:
        update.effective_message.reply_html(Message.INVALID_TEXT)


def send_help(update: Update, _):

    text = open("data/help.html").read()
    update.message.reply_html(text=text)


def send_start(update: Update, _):

    name = update.effective_user.full_name
    text = open("data/start.html").read().format(NAME=name)
    update.message.reply_html(text=text)


def start_fiction(update: Update, context: CallbackContext):

    clear_previous_state(context)
    context.user_data["sessionType"] = Constants.FICTION_SESSION
    context.user_data["newMessage"] = True
    start(update, context)


def start_nonfiction(update: Update, context: CallbackContext):

    clear_previous_state(context)
    context.user_data["sessionType"] = Constants.NONFICTION_SESSION
    context.user_data["newMessage"] = True
    start(update, context)


def start_short_story(update: Update, context: CallbackContext):

    clear_previous_state(context)
    context.user_data["sessionType"] = Constants.SHORT_STORY_SESSION
    context.user_data["newMessage"] = True
    start(update, context)


def stay_awake_ping(_, __):

    logging.info("Got ping to stay awake")
