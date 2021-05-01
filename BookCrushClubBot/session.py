from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import PARSEMODE_HTML as HTML
from telegram.ext import CallbackContext
from .button import Button
from .constants import Constants
from .label import Label
from .message import Message


def start(update: Update, context: CallbackContext):

    base_message = context.user_data.get("baseMessage", None)
    database = context.bot_data["database"]
    chat = update.effective_chat
    sess_type = context.user_data["sessionType"]
    user_id = update.effective_user.id

    if sess_type == Constants.FICTION_SESSION:
        genre = Constants.FICTION_GENRE
        max_count = Constants.FICTION_COUNT
    elif sess_type == Constants.NONFICTION_SESSION:
        genre = Constants.NONFICTION_GENRE
        max_count = Constants.NONFICTION_COUNT

    if base_message:
        books_iter = context.user_data["books"]
    else:
        if sess_type == Constants.FICTION_SESSION:
            books_iter = database.get_fiction_books(user_id)
        elif sess_type == Constants.NONFICTION_SESSION:
            books_iter = database.get_nonfiction_books(user_id)

    books = []
    books_str = []
    count = 0

    for book_name, authors in books_iter:
        authors_str = " ,".join(authors)
        books.append((book_name, authors))
        books_str.append(Message.BOOK.format(BOOK_NAME=book_name, AUTHORS=authors_str))
        count += 1

    context.user_data["books"] = books
    books_txt = "\n".join(books_str)

    if count == 0:
        text = Message.EMPTY_SUGGESTIONS.format(GENRE=genre)
        buttons = InlineKeyboardMarkup.from_button(Button.SUGGEST)
    elif count < max_count:
        left = max_count - count
        s = "s" * (left != 1)
        text = Message.HALF_SUGGESTIONS.format(
            BOOKS=books_txt, GENRE=genre, LEFT=left, S=s
        )
        buttons = InlineKeyboardMarkup.from_row([Button.SUGGEST, Button.REMOVE])
    else:
        s = "s" * (max_count != 1)
        text = Message.FULL_SUGGESTIONS.format(BOOKS=books_txt, GENRE=genre, S=s)
        buttons = InlineKeyboardMarkup.from_button(Button.REMOVE, COUNT=count)

    if context.user_data.pop("newMessage", False):
        base_msg = chat.send_message(text=text, reply_markup=buttons, parse_mode=HTML)
    else:
        base_msg = base_message.edit_text(
            text=text, reply_markup=buttons, parse_mode=HTML
        )
    context.user_data["baseMessage"] = base_msg


def remove(update: Update, context: CallbackContext):

    base_message = context.user_data["baseMessage"]
    update.callback_query.answer()
    buttons = [
        InlineKeyboardButton(text=name, callback_data=f"remove_{ix}")
        for ix, (name, _) in enumerate(context.user_data["books"])
    ]
    back = InlineKeyboardButton(text=Label.BACK, callback_data="start")
    buttons.append(back)
    keyboard = InlineKeyboardMarkup.from_column(buttons)
    base_msg = base_message.edit_text(
        text=Message.REMOVE_BOOKS, reply_markup=keyboard, parse_mode=HTML
    )
    context.user_data["baseMessage"] = base_msg


def remove_book(update: Update, context: CallbackContext):

    database = context.bot_data["database"]
    sess_type = context.user_data["sessionType"]
    user_id = update.effective_user.id
    ix = int(update.callback_query.data.lstrip("remove_"))
    name, _ = context.user_data["books"].pop(ix)

    if sess_type == Constants.FICTION_SESSION:
        database.remove_fiction_book(user_id, name)
    elif sess_type == Constants.NONFICTION_SESSION:
        database.remove_nonfiction_book(user_id, name)

    update.callback_query.answer(Message.REMOVED_BOOK.format(BOOK_NAME=name))
    start(update, context)


def suggest(update: Update, context: CallbackContext):

    base_message = context.user_data["baseMessage"]
    update.callback_query.answer()
    buttons = [[Button.SUGGEST_ISBN, Button.SUGGEST_NAME, Button.SUGGEST_RAW]]
    back = InlineKeyboardButton(text=Label.BACK, callback_data="start")
    buttons.append([back])
    keyboard = InlineKeyboardMarkup(buttons)
    base_msg = base_message.edit_text(
        text=Message.SUGGESTIONS_METHOD, reply_markup=keyboard, parse_mode=HTML
    )
    context.user_data["baseMessage"] = base_msg


def suggest_book(update: Update, context: CallbackContext):

    context.user_data["baseMessage"].edit_reply_markup()
    database = context.bot_data["database"]
    sess_type = context.user_data["sessionType"]
    user = update.effective_user
    user_id = user.id
    fullname = user.full_name
    ix = int(update.callback_query.data.lstrip("suggest_"))
    name, authors, genres = context.user_data.pop("results")[ix]

    if sess_type == Constants.FICTION_SESSION:
        database.add_fiction_book(user_id, fullname, name, authors, genres, None)
    elif sess_type == Constants.NONFICTION_SESSION:
        database.add_nonfiction_book(user_id, fullname, name, authors, genres, None)

    update.callback_query.answer(Message.ADDED_BOOK.format(BOOK_NAME=name))
    context.user_data["books"].append((name, authors))
    context.user_data["newMessage"] = True
    start(update, context)
