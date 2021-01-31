import logging
from telegram import Update
from telegram.ext import CallbackContext
from .constants import Constants
from .message import Message
from .session import start


def clear_previous_state(context: CallbackContext):

    msg = context.user_data.pop("baseMessage", None)
    if msg:
        msg.edit_reply_markup()
    context.user_data.clear()


def redirect_update(update: Update, context: CallbackContext):

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
    text = open("data/start.html").read().format(NAME=full_name)
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


def stay_awake_ping(_, __):

    logging.info("Got ping to stay awake")
