import logging
from time import sleep
from telegram import Update
from telegram.error import TelegramError
from telegram.ext import CallbackContext
from .constants import Constants
from .message import Message
from .session import start


def __get_items(session: str, update: Update, context: CallbackContext):

    if update.message.chat.id != Constants.ADMINS_GROUP:
        update.message.reply_text(text=Message.UNAUTHORIZED_COMMAND)
        return

    database = context.bot_data["database"]
    genre = ""
    items = []

    if session == Constants.FICTION_SESSION:
        genre = "Fiction"
        items = database.get_fiction_books_all()
    elif session == Constants.NONFICTION_SESSION:
        genre = "Non Fiction"
        items = database.get_nonfiction_books_all()
    elif session == Constants.SHORT_STORY_SESSION:
        genre = "Short Story"
        items = database.get_short_stories_all()

    splits = []
    count = 0
    for (book, authors, names) in items:
        book_full = Message.BOOK_FULL.format(
            BOOK_NAME=book, AUTHORS=", ".join(authors), NAMES=", ".join(names)
        )
        splits.append(book_full)
        count += 1

    books = "\n".join(splits)
    text = Message.BOOKS_DISPLAY.format(GENRE=genre, BOOKS=books, TOTAL=count)
    update.message.reply_html(text)


def announce(update: Update, context: CallbackContext):

    if update.message.chat.id != Constants.ADMINS_GROUP:
        update.message.reply_text(text=Message.UNAUTHORIZED_COMMAND)
        return

    msg = update.message.reply_to_message
    if not msg:
        update.message.reply_text(Message.ANNOUNCEMENT_NO_REPLY)
        return

    update.message.reply_text(Message.ANNOUNCEMENT_STARTED)

    database = context.bot_data["database"]
    users = database.get_users()
    count = 0
    total = 0

    for (user_id,) in users:
        try:
            msg.copy(user_id)
            sleep(Constants.DELAY)
        except TelegramError:
            pass
        else:
            count += 1
        total += 1

    update.message.reply_text(
        Message.ANNOUNCEMENT_DONE.format(COUNT=count, TOTAL=total)
    )


def clear_database(update: Update, context: CallbackContext):

    arg = context.args[0] if context.args else None
    database = context.bot_data["database"]

    if arg == "fiction":
        database.clear_fiction_books()
    elif arg == "nonfiction":
        database.clear_nonfiction_books()
    elif arg == "shortstory":
        database.clear_short_stories()
    else:
        update.message.reply_html(Message.CLEAR_ERROR)
        return
    update.message.reply_html(Message.CLEAR_DONE.format(SECTION=arg))


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


def send_start(update: Update, context: CallbackContext):

    if context.args:
        arg = context.args[0]
        if arg == "fiction":
            start_fiction(update, context)
        elif arg == "nonfiction":
            start_nonfiction(update, context)
        elif arg == "shortstory":
            start_short_story(update, context)
        else:
            logging.info("Incorrect start payload %s", arg)
    else:
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
