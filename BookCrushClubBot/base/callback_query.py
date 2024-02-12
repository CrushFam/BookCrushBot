"""Handlers for callback query."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
import BookCrushClubBot

from BookCrushClubBot.constants import (CallbackData, Key, Label, Literal,
                                        Message)


async def action_remove(update: Update, context: CallbackContext):
    """Show list of books for user to remove."""
    await update.callback_query.answer()
    database = context.bot_data["database"]
    sect = context.user_data["section"]
    user_id = update.callback_query.from_user.id
    message = update.callback_query.message
    books = database.get_books(user_id, sect)
    context.user_data["books"] = books
    books_txt = "\n".join(
        Message.BOOK.format(NAME=name, AUTHOR=auth) for (name, auth) in books
    )
    txt = Message.CONFIRM_REMOVE.format(BOOKS=books_txt)
    buttons = [
        InlineKeyboardButton(
            text=Label.BOOK.format(NAME=name),
            callback_data=CallbackData.CONFIRM_REMOVE.format(IX=ix),
        )
        for ix, (name, _) in enumerate(books)
    ]
    back = InlineKeyboardButton(
        text=Label.BACK, callback_data=CallbackData.CHOOSE_ACTION.format(SECTION=sect)
    )
    buttons.append(back)
    markup = InlineKeyboardMarkup.from_column(buttons)
    await message.edit_text(text=txt, reply_markup=markup)


async def action_suggest(update: Update, context: CallbackContext):
    """Prompt user to suggest an book."""
    await update.callback_query.answer()
    sect = context.user_data["section"]
    message = update.callback_query.message
    back = InlineKeyboardButton(
        text=Label.BACK, callback_data=CallbackData.CHOOSE_ACTION.format(SECTION=sect)
    )
    context.user_data["expectingInput"] = True
    markup = InlineKeyboardMarkup.from_button(back)
    await message.edit_text(text=Message.SUGGEST_BOOK, reply_markup=markup)


async def choose_action(update: Update, context: CallbackContext, skip: bool = False):
    """Show user actions to perform on a section."""
    database = context.bot_data["database"]
    user_id = (
        update.callback_query.from_user.id
        if update.callback_query
        else update.message.from_user.id
    )
    message = update.callback_query.message if update.callback_query else update.message

    if skip:
        sect = context.user_data["section"]
    else:
        await update.callback_query.answer()
        sect = update.callback_query.data.split("_")[-1]
        context.user_data["section"] = sect

    sect_name = Literal.SECTIONS[sect]
    genre = database.get_value(Key.GENRE.value.format(SECTION=sect))
    maxc = int(database.get_value(Key.MAX_SUGGESTIONS.value.format(SECTION=sect)))
    books = database.get_books(user_id, sect)
    books_txt = "\n".join(
        Message.BOOK.format(NAME=name, AUTHOR=auth) for (name, auth) in books
    )
    suggested = len(books)
    buttons = [
        [
            InlineKeyboardButton(
                text=Label.SUGGEST, callback_data=CallbackData.ACTION_SUGGEST
            ),
            InlineKeyboardButton(
                text=Label.REMOVE, callback_data=CallbackData.ACTION_REMOVE
            ),
        ],
        [
            InlineKeyboardButton(
                text=Label.BACK, callback_data=CallbackData.CHOOSE_SECTION
            )
        ],
    ]

    if suggested == 0:
        buttons[0].pop(1)
        text = Message.SUGGESTIONS_ZERO.format(GENRE=genre, SECTION=sect_name)
    elif suggested < maxc:
        more = maxc - suggested
        text = Message.SUGGESTIONS_PARTIAL.format(
            GENRE=genre, SECTION=sect_name, BOOKS=books_txt, COUNT=more
        )
    else:
        buttons[0].pop(0)
        text = Message.SUGGESTIONS_FULL.format(
            GENRE=genre, SECTION=sect_name, BOOKS=books_txt
        )
    markup = InlineKeyboardMarkup(buttons)

    if update.callback_query:
        await message.edit_text(text=text, reply_markup=markup)
    else:
        msg = await context.bot.send_message(
            chat_id=user_id, text=text, reply_markup=markup
        )
        context.user_data["baseMessage"] = msg


async def confirm_remove(update: Update, context: CallbackContext):
    """Remove the book from the database."""
    database = context.bot_data["database"]
    ix = int(update.callback_query.data.split("_")[1])
    books = context.user_data.pop("books")
    name, author = books.pop(ix)
    user_id = update.callback_query.from_user.id
    sect = context.user_data["section"]
    ret = database.remove_book(user_id, sect, name, author)
    await BookCrushClubBot.base.command.sync_poll(update, context)
    
    if ret:
        text = Message.REMOVED_BOOK.format(NAME=name)
    else:
        text = Message.UNKNOWN_ERROR

    await update.callback_query.answer(text=text)
    await choose_action(update, context, True)


async def confirm_suggest(update: Update, context: CallbackContext):
    """Suggest the book to the database."""
    context.user_data.pop("expectingInput", None)
    database = context.bot_data["database"]
    ix = int(update.callback_query.data.split("_")[1])
    books = context.user_data.pop("books")
    name, author = books.pop(ix)
    user_id = update.callback_query.from_user.id
    sect = context.user_data["section"]
    ret = database.add_book(user_id, sect, name.title(), author.title())
    await BookCrushClubBot.base.command.sync_poll(update, context)
    if ret:
        text = Message.SUGGESTED_BOOK.format(NAME=name)
    else:
        text = Message.UNKNOWN_ERROR

    await update.callback_query.answer(text=text)
    await choose_action(update, context, True)
