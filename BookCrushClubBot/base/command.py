"""Handler for commands."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

from BookCrushClubBot.constants import CallbackData, Key, Literal, Message
from BookCrushClubBot.utils.misc import broadcast_pulse

from .callback_query import choose_action


async def books(update: Update, context: CallbackContext):
    """Show sections available for suggestion."""
    msg = context.user_data.pop("baseMessage", None)
    if msg:
        await msg.edit_reply_markup()

    if update.callback_query:
        await update.callback_query.answer()
        user_id = update.callback_query.from_user.id
        message = update.callback_query.message
    else:
        user_id = update.message.from_user.id
        message = update.message

    markup = InlineKeyboardMarkup.from_row(
        [
            InlineKeyboardButton(
                text=v, callback_data=CallbackData.CHOOSE_ACTION.format(SECTION=k)
            )
            for (k, v) in Literal.SECTIONS.items()
        ]
    )

    if update.callback_query:
        msg = await message.edit_text(text=Message.CHOOSE_SECTION, reply_markup=markup)
    else:
        msg = await context.bot.send_message(
            chat_id=user_id,
            text=Message.CHOOSE_SECTION,
            reply_markup=markup,
        )

    context.user_data["baseMessage"] = msg


async def broadcast(update: Update, context: CallbackContext):
    """Broadcast the quoted message to all users."""
    if not update.message.reply_to_message:
        await update.message.reply_text(Message.INVALID_MESSAGE)
        return

    database = context.bot_data["database"]
    users = database.get_users()
    context.bot_data["broadcastMessage"] = update.message.reply_to_message
    context.bot_data["broadcastUsers"] = users
    context.bot_data["broadcastCommand"] = update.message
    context.bot_data["broadcastSuccess"] = 0
    context.bot_data["broadcastFailed"] = 0
    context.job_queue.run_repeating(broadcast_pulse, Literal.BROADCAST_INTERVAL)
    await update.message.reply_text(Message.BROADCAST_STARTED.format(TOTAL=len(users)))


async def clear(update: Update, context: CallbackContext):
    """Clear books of a section."""
    database = context.bot_data["database"]
    sect = " ".join(context.args).lower() if context.args else None
    sects = ", ".join((Message.MONO.format(TERM=sect) for sect in Literal.SECTIONS))

    if sect in Literal.SECTIONS:
        database.clear_section(sect)
        await update.message.reply_text(Message.CLEARED_SECTION.format(SECTION=sect))
    else:
        await update.message.reply_text(
            Message.INVALID_SECTION.format(SECTION=sect, SECTIONS=sects)
        )


async def get(update: Update, context: CallbackContext):
    """Get the value of a key."""
    database = context.bot_data["database"]
    key = context.args[-1].lower() if context.args else None
    value = database.get_value(key)
    keys = ", ".join((Message.MONO.format(TERM=key) for key in Literal.KEYS))

    if value:
        text = value
    else:
        text = Message.INVALID_KEY.format(KEY=key, KEYS=keys)

    await update.message.reply_text(text)


async def help_(update: Update, context: CallbackContext):
    """Send the help message."""
    chat = update.message.chat

    if chat.type == chat.PRIVATE:
        await update.message.reply_text(Message.HELP_PRIVATE)
    else:
        await update.message.reply_text(Message.HELP_ADMINS)


async def list_(update: Update, context: CallbackContext):
    """List books of a section."""
    database = context.bot_data["database"]
    sect = " ".join(context.args).lower() if context.args else None
    sects = ", ".join((Message.MONO.format(TERM=sect) for sect in Literal.SECTIONS))

    if sect in Literal.SECTIONS:
        books = database.list_section(sect)
        count = len(books)
        books_txt = "\n".join(
            (
                Message.BOOK_VERBOSE.format(
                    NAME=name, AUTHORS=auths, USERS=", ".join(users)
                )
                for (name, auths, users) in books
            )
        )
        text = Message.LIST_SECTION.format(BOOKS=books_txt, COUNT=count)
        await update.message.reply_text(text)
    else:
        await update.message.reply_text(
            Message.INVALID_SECTION.format(SECTION=sect, SECTIONS=sects)
        )


async def set_(update: Update, context: CallbackContext):
    """Set the value of a key."""
    database = context.bot_data["database"]
    reply = update.message.reply_to_message
    key = context.args[0].lower() if context.args else None
    value = (
        " ".join(context.args[1:])
        if len(context.args) >= 2
        else reply.text_html_urled
        if reply
        else None
    )
    keys = ", ".join((Message.MONO.format(TERM=key) for key in Literal.KEYS))

    if key:
        if value:
            if database.set_value(key, value):
                text = text = Message.SET_KEY.format(KEY=key)
            else:
                text = Message.INVALID_KEY.format(KEY=key, KEYS=keys)
        else:
            text = Message.INVALID_VALUE
    else:
        text = Message.INVALID_KEY.format(KEY=key, KEYS=keys)

    await update.message.reply_text(text)


async def start(update: Update, context: CallbackContext):
    """Send the start message."""
    database = context.bot_data["database"]
    chat = update.message.chat
    start = database.get_value(Key.START_TEXT.value)
    user_id = update.message.from_user.id
    name = update.message.from_user.full_name
    sect = context.args[0].lower() if context.args else None
    database.add_user(user_id, name)

    if sect in Literal.SECTIONS:
        context.user_data["section"] = sect
        await choose_action(update, context, True)
        return

    if chat.type == chat.PRIVATE:
        await update.message.reply_text(start.replace("FULL_NAME", name))
    else:
        await update.message.reply_text(Message.START)
