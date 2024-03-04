"""Miscellaneous functions."""

from datetime import date
from datetime import time as ttime
import logging
import random, string

from bs4 import BeautifulSoup
import BookCrushClubBot

import requests
from telegram import Update, ChatJoinRequest
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

async def schedule_jobs (update: Update, context: CallbackContext):
    if(update.message.chat.id == 15024063):
        context.job_queue.run_daily(callback=send_random_quote, time = ttime(hour=12, minute=30, second=0, microsecond=0), chat_id=Literal.BOOKCRUSHCLUB_CHAT_ID, name = "send_random_quote")
        await update.message.reply_text("Scheduled random quote daily at 6pm.") 

async def send_random_quote (context: CallbackContext):
    database = context.bot_data["database"]
    authors = database.get_authors()
    authors = [x[0] for x in authors]
    print(authors)
    msg = random.choice(authors)
    url = "http://www.goodreads.com/quotes/search?utf8=%E2%9C%93&q=" + msg
    req = requests.get(url)
    soup = BeautifulSoup(req.content)
    
    #get quotes from page
    div_quotes = soup("div", attrs={"class":"quoteText"}) #soup("div") == soup.find_all("div")
    quotes = ''
    for q in div_quotes:
        author = ""
        # If no author, then skip
        try:
            author = q.find("span").get_text().strip() + " " + "<b>" + q.find("a").get_text() + "</b>\n"
            #print(q.find("span").get_text())
        except:
            continue
        quote = ""
        # turn multiline quotes/poems into a single string
        for i in range(len(q.contents)):
            #find returns
            line = q.contents[i].encode("ascii", errors="ignore").decode("utf-8")
            #print("line ", line)
            if (line[0] == "<"): # is tag, ignore characters that aren't part of quote 
                break
            else:
                quote += line

        quote = q.contents[0].encode("ascii", errors="ignore").decode("utf-8")
        quote = "\"" + quote.strip() + "\""
        quotes += "<blockquote><i>" + quote + "</i></blockquote>" + '\n\n' + '- ' + author.strip() + "#"
    quotes_to_return = filter(lambda x: x in string.printable, quotes)
    quotes = "".join(quotes_to_return).split("#")
    if not quotes.isalnum(): return
    finalquote = random.choice(quotes) + '\n\n' + '#Quotes'
    await context.bot.send_message(Literal.BOOKCRUSHCLUB_CHAT_ID, finalquote)

async def decline(update: Update, context: CallbackContext):
    print("test")
    await update.chat_join_request.decline()
    
