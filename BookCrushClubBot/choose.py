from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import CHATACTION_TYPING as TYPING, PARSEMODE_HTML as HTML
from telegram.ext import CallbackContext
from .constants import Constants
from .label import Label
from .message import Message
from .utils import get_book_by_isbn, get_books_by_name


def parse_raw(update: Update, context: CallbackContext):

    context.user_data["baseMessage"].edit_reply_markup()
    item = (
        "story"
        if context.user_data["sessionType"] == Constants.SHORT_STORY_SESSION
        else "book"
    )
    chat = update.effective_chat
    details = update.message.text
    lx = details.splitlines()
    buttons = [InlineKeyboardButton(text=Label.BACK, callback_data="suggest")]

    if len(lx) == 3:
        name = lx[0]
        authors = lx[1].split(",")
        genres = lx[2].split(",")
        authors_str = " ,".join(authors)
        context.user_data["results"] = [(name, authors, genres)]
        book = Message.BOOK.format(BOOK_NAME=name, AUTHORS=authors_str)
        text = Message.CONFIRM_BOOK.format(BOOK=book, ITEM=item)
        buttons.insert(
            0, InlineKeyboardButton(text=Label.YES, callback_data="suggest_0")
        )
    else:
        text = Message.INVALID_RAW_FORMAT

    keyboard = InlineKeyboardMarkup.from_row(buttons)
    context.user_data["redirectUpdate"] = parse_raw
    base_msg = chat.send_message(text=text, reply_markup=keyboard, parse_mode=HTML)
    context.user_data["baseMessage"] = base_msg


def search_by_isbn(update: Update, context: CallbackContext):

    context.user_data["baseMessage"].edit_reply_markup()
    item = (
        "story"
        if context.user_data["sessionType"] == Constants.SHORT_STORY_SESSION
        else "book"
    )
    chat = update.effective_chat
    query = update.message.text
    chat.send_action(TYPING)
    res = get_book_by_isbn(query)
    query = query.replace(" ", "+")
    buttons = [InlineKeyboardButton(text=Label.BACK, callback_data="suggest")]

    if res:
        name = res[0]
        authors = res[1]
        genres = res[2]
        authors_str = " ,".join(authors)
        context.user_data["results"] = [(name, authors, genres)]
        book = Message.BOOK.format(BOOK_NAME=name, AUTHORS=authors_str)
        text = Message.CONFIRM_BOOK.format(BOOK=book, ITEM=item)
        buttons.insert(
            0, InlineKeyboardButton(text=Label.YES, callback_data="suggest_0")
        )
    else:
        text = Message.NO_RESULTS.format(QUERY=query)

    keyboard = InlineKeyboardMarkup.from_row(buttons)
    context.user_data["redirectUpdate"] = search_by_isbn
    base_msg = chat.send_message(
        text=text, reply_markup=keyboard, parse_mode=HTML, disable_web_page_preview=True
    )
    context.user_data["baseMessage"] = base_msg


def search_by_name(update: Update, context: CallbackContext):

    context.user_data["baseMessage"].edit_reply_markup()
    item = (
        "stories"
        if context.user_data["sessionType"] == Constants.SHORT_STORY_SESSION
        else "books"
    )
    chat = update.effective_chat
    query = update.message.text
    chat.send_action(TYPING)
    results = context.user_data["results"] = get_books_by_name(query)
    query = query.replace(" ", "+")
    buttons = []
    text_bits = []

    for ix, (name, authors, _) in enumerate(results):
        authors_str = " ,".join(authors)
        book_dt = Message.BOOK.format(BOOK_NAME=name, AUTHORS=authors_str)
        text_bits.append(book_dt)
        button = InlineKeyboardButton(text=name, callback_data=f"suggest_{ix}")
        buttons.append(button)

    buttons.insert(0, InlineKeyboardButton(text=Label.BACK, callback_data="suggest"))

    if results:
        books_txt = "\n".join(text_bits)
        text = Message.SEARCH_RESULTS.format(BOOKS=books_txt, ITEM=item, QUERY=query)
    else:
        text = Message.NO_RESULTS.format(QUERY=query)

    keyboard = InlineKeyboardMarkup.from_column(buttons)
    base_msg = chat.send_message(
        text=text, reply_markup=keyboard, parse_mode=HTML, disable_web_page_preview=True
    )
    context.user_data["baseMessage"] = base_msg
    context.user_data["redirectUpdate"] = search_by_name


def suggest_by_isbn(update: Update, context: CallbackContext):

    base_message = context.user_data["baseMessage"]
    item = (
        "story"
        if context.user_data["sessionType"] == Constants.SHORT_STORY_SESSION
        else "book"
    )
    update.callback_query.answer()
    back = InlineKeyboardButton(text=Label.BACK, callback_data="suggest")
    keyboard = InlineKeyboardMarkup.from_button(back)
    context.user_data["redirectUpdate"] = search_by_isbn
    base_msg = base_message.edit_text(
        text=Message.SEARCH_ISBN.format(ITEM=item),
        reply_markup=keyboard,
        parse_mode=HTML,
    )
    context.user_data["baseMessage"] = base_msg


def suggest_by_name(update: Update, context: CallbackContext):

    base_message = context.user_data["baseMessage"]
    item = (
        "story"
        if context.user_data["sessionType"] == Constants.SHORT_STORY_SESSION
        else "book"
    )
    update.callback_query.answer()
    back = InlineKeyboardButton(text=Label.BACK, callback_data="suggest")
    keyboard = InlineKeyboardMarkup.from_button(back)
    context.user_data["redirectUpdate"] = search_by_name
    base_msg = base_message.edit_text(
        text=Message.SEARCH_NAME.format(ITEM=item),
        reply_markup=keyboard,
        parse_mode=HTML,
    )
    context.user_data["baseMessage"] = base_msg


def suggest_raw(update: Update, context: CallbackContext):

    base_message = context.user_data["baseMessage"]
    item = (
        "story"
        if context.user_data["sessionType"] == Constants.SHORT_STORY_SESSION
        else "book"
    )
    update.callback_query.answer()
    back = InlineKeyboardButton(text=Label.BACK, callback_data="suggest")
    keyboard = InlineKeyboardMarkup.from_button(back)
    context.user_data["redirectUpdate"] = parse_raw
    base_msg = base_message.edit_text(
        text=Message.SUGGEST_RAW.format(ITEM=item),
        reply_markup=keyboard,
        parse_mode=HTML,
    )
    context.user_data["baseMessage"] = base_msg
