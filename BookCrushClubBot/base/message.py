"""Handlers for non-command messages."""

from telegram import (ChatAction, InlineKeyboardButton, InlineKeyboardMarkup,
                      Update)
from telegram.ext import CallbackContext

from BookCrushClubBot.constants import CallbackData, Label, Message
from BookCrushClubBot.utils.misc import parse_text, search_book


def _display_results(update: Update, context: CallbackContext):
    """Display results for user to select."""
    message = context.user_data["baseMessage"]
    sect = context.user_data["section"]
    books = context.user_data["books"]

    if books:
        books_txt = "\n".join(
            Message.BOOK.format(NAME=name, AUTHOR=auth) for (name, auth) in books
        )
        txt = Message.CONFIRM_SUGGEST.format(BOOKS=books_txt)
        buttons = [
            InlineKeyboardButton(
                text=Label.BOOK.format(NAME=name),
                callback_data=CallbackData.CONFIRM_SUGGEST.format(IX=ix),
            )
            for ix, (name, _) in enumerate(books)
        ]
    else:
        txt = Message.NO_RESULTS
        buttons = []

    back = InlineKeyboardButton(
        text=Label.BACK, callback_data=CallbackData.CHOOSE_ACTION.format(SECTION=sect)
    )
    buttons.append(back)
    markup = InlineKeyboardMarkup.from_column(buttons)
    message.edit_reply_markup()
    msg = message.reply_text(text=txt, reply_markup=markup)
    context.user_data["baseMessage"] = msg


def handle_text(update: Update, context: CallbackContext):
    """Handle text messages."""
    if context.user_data.get("expectingInput", False):
        name, authors = parse_text(update.message.text)
        if authors:
            results = [(name, authors)]
        else:
            update.message.chat.send_action(ChatAction.TYPING)
            results = search_book(name, authors)
        context.user_data["books"] = results
        _display_results(update, context)
    else:
        fallback(update, context)


def fallback(update: Update, context: CallbackContext):
    """Fallback handler for all messages."""
    update.message.reply_text(Message.UNEXPECTED_MESSAGE)
