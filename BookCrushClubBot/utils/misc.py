"""Miscellaneous functions."""

import logging

import requests
from telegram.error import TelegramError
from telegram.ext import CallbackContext

from BookCrushClubBot.constants import Literal, Message


def _parse_doc(doc):
    """Return parsed (name, author)."""
    title = doc["title"][: Literal.MAX_BOOK_NAME]
    author = ", ".join(set(doc.get("author_name", ())))[: Literal.MAX_AUTHOR_NAME]
    return (title, author)


async def broadcast_pulse(context: CallbackContext):
    """Broadcast the message to one user."""
    try:
        user_id = context.bot_data["broadcastUsers"].pop()
    except IndexError:
        command = context.bot_data.pop("broadcastCommand")
        success = context.bot_data.pop("broadcastSuccess")
        failed = context.bot_data.pop("broadcastFailed")
        del context.bot_data["broadcastMessage"]
        context.job.schedule_removal()
        rate = int((success / (success + failed)) * 100)
        text = Message.BROADCAST_COMPLETED.format(RATE=rate)
        await command.reply_text(text)
    else:
        message = context.bot_data["broadcastMessage"]
        try:
            await message.copy(user_id)
        except TelegramError:
            context.bot_data["broadcastFailed"] += 1
        else:
            context.bot_data["broadcastSuccess"] += 1


def parse_text(text: str):
    """Parse given text and return (name, author)."""
    lines = text.splitlines()

    if len(lines) == 1:
        name = lines[0].strip()
        author = ""
    else:
        name = lines[0].strip()
        author = lines[1].strip()

    return (name, author)


def search_book(name: str, author: str):
    """Return a list of books matching the given values."""
    params = Literal.OPEN_LIBRARY_PARAMS
    params["q"] = name

    try:
        req = requests.get(Literal.OPEN_LIBRARY_URL, params).json()["docs"][:5]
        res = [
            _parse_doc(doc) for doc in req if "title" in doc and "author_name" in doc
        ]
    except Exception as e:
        logging.error(e)
        return []
    else:
        return res
