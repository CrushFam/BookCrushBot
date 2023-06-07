"""Handler for commands."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

from BookCrushClubBot.constants import CallbackData, Key, Literal, Message
from BookCrushClubBot.utils.misc import broadcast_pulse

from .callback_query import choose_action
import re
import requests
import datetime
from bs4 import BeautifulSoup

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


def peek(bookname):
    url = f"https://app.thestorygraph.com/browse?search_term={bookname}"
    sp = requests.get(url).content
    soup = BeautifulSoup(sp, 'lxml')
    divi = soup.find('div', class_ = 'book-pane-content')
    img = divi.find('img').get('src')
    divi = divi.find('div', class_ = 'book-title-author-and-series')
    bli = divi.find('a')
    bname = bli.text
    aname = divi.find('p','font-body').text.strip()
    try:
        seriesname = divi.find('p','font-semibold').text
    except:
        seriesname = 'N/A'
    burl = 'https://app.thestorygraph.com' + bli.get('href')
    return (bname,seriesname,aname,img,burl)

def mine(burl):
    bp = BeautifulSoup(requests.get(burl).content, 'lxml')
    sr = bp.find('span','average-star-rating').text.strip()
    pre = '<div class="trix-content mt-3"><div>'.strip()
    post = "</div>".strip()
    pattern = pre +' *(.|\n)+ *'+post
    blurb = bp.find('div','blurb-pane').parent.find('script').text
    inht = re.search(pattern, blurb).group().replace('\\',"")
    desc = BeautifulSoup(inht,'lxml').text
    return (sr,desc)

def genpost(bookname):
    bname,seriesname, aname,img,burl = peek(bookname)
    sr,desc = mine(burl)
    star = "⭐"*round(float(sr))
    ser=""
    if seriesname != 'N/A':
        ser = \
f"""
<b><i>{seriesname}</b><i>"""
        
    post = \
f"""\
<b>{bname}</b>{ser}
<i>{aname}</i>

{star} ({sr}/5.00)

{desc}
"""
    return (img,post,burl)



async def mkposts(update: Update, context: CallbackContext):
    """Make post with data extracted from goodreads"""
    database = context.bot_data["database"]
    sect = " ".join(context.args).lower() if context.args else None
    sects = ", ".join((Message.MONO.format(TERM=sect) for sect in Literal.SECTIONS))

    if sect in Literal.SECTIONS:
        books = database.list_section(sect)
        
        for (name, auths, users) in books:
            img,post,link = genpost(name + ' ' +auths)
            link="<a href='"+link+"'>read more</a>"
            caplen=len(post)
            linklen=len(link)
            if (caplen + linklen) >1024:
                limit = 1024 - linklen -5
                post = post[:limit] + '...\n'
            post+=link
            await update.message.reply_photo(img,post)

        await update.message.reply_text("completed making posts")
    else:
        await update.message.reply_text(
            Message.INVALID_SECTION.format(SECTION=sect, SECTIONS=sects)
        )


async def getbookinfo(update: Update, context: CallbackContext):
    """Get post for any book"""
    bname = " ".join(context.args).lower() if context.args else None

    if bname:
        img,post,link = genpost(bname)
        link="<a href='"+link+"'>read more</a>"
        caplen=len(post)
        linklen=len(link)
        if (caplen + linklen) >1024:
            limit = 1024 - linklen -5
            post = post[:limit] + '...\n'
        post+=link
        await update.message.reply_photo(img,post)
    else:
        await update.message.reply_text("Sorry no such books found")


async def botmpost(update: Update, context: CallbackContext):
    """Get post for any book"""
    bname = " ".join(context.args).lower() if context.args else None

    if bname:
        img,post,link = genpost(bname)
        link="<a href='"+link+"'>read more</a>"
        date= datetime.datetime.now()
        header = f"<b><u>BOTM - {date.strftime('%b')} {date.year} </b><u>\n\n"
        post=header+post
        caplen=len(post)
        linklen=len(link)
        if (caplen + linklen) >1024:
            limit = 1024 - linklen -5
            post = post[:limit] + '...\n'
        post+=link
        await update.message.reply_photo(img,post)
    else:
        await update.message.reply_text("Sorry no such books found")


async def rltpost(update: Update, context: CallbackContext):
    """Get post for any book"""
    bname = " ".join(context.args).lower() if context.args else None

    if bname:
        img,post,link = genpost(bname)
        link="<a href='"+link+"'>read more</a>"
        date= datetime.datetime.now()
        header = f"<b><u>Roulette - {date.strftime('%b')} {date.year} </b></u>\n\n"
        post=header+post
        caplen=len(post)
        linklen=len(link)
        if (caplen + linklen) >1024:
            limit = 1024 - linklen -5
            post = post[:limit] + '...\n'
        post+=link
        await update.message.reply_photo(img,post)
    else:
        await update.message.reply_text("Sorry no such books found")


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
