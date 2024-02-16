"""Handler for commands."""
import langdetect 
import pyphen
import requests, string, random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

from BookCrushClubBot.constants import CallbackData, Key, Literal, Message, Label
from BookCrushClubBot.utils.misc import broadcast_pulse

from .callback_query import choose_action
import re
import asyncio
import httpx
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
                    NAME=name.title(), AUTHORS=auths.title(), USERS=", ".join(users)
                )
                for (name, auths, users) in books
            )
        )
        # to display in a format that can be input for ultimate-poll-bot
        pollbot_dest = "\n". join(
            (
                Message.POLLBOT_VERBOSE.format(
                    NAME=name.title(), AUTHORS=auths.title(), USERS=" "
                )
                for (name, auths, users) in books
            )
        )
        text = Message.LIST_SECTION.format(BOOKS=books_txt, COUNT=count)
        await update.message.reply_text(text)
        await update.message.reply_text("<code>" + pollbot_dest + "</code>")
        await sync_poll(update, context)
    else:
        await update.message.reply_text(
            Message.INVALID_SECTION.format(SECTION=sect, SECTIONS=sects)
        )

async def poll (update: Update, context: CallbackContext):
    database = context.bot_data["polldb"]
    print(database)
    await update.message.reply_text("testing")
    id = Literal.LINKED_POLL
    poll = database.get_poll(id)
    print("reaching here?")
    await update.message.reply_text(poll)

async def sync_poll (update: Update, context: CallbackContext):
    polldb = context.bot_data["polldb"]
    id = Literal.LINKED_POLL
    database = context.bot_data["database"]
    sect = " ".join(context.args).lower() if context.args else "botm"
    sects = ", ".join((Message.MONO.format(TERM=sect) for sect in Literal.SECTIONS))
    success = False
    if sect in Literal.SECTIONS:
        books = database.list_section(sect)
        id = Literal.LINKED_POLL
        if(polldb.get_max_index(id) == None):
            index = 0
        else:
            index = polldb.get_max_index(id) + 1
        for (name, auth, user) in books:
            success = polldb.sync(id, index, name.title(), auth.title())
            index = index + 1
        
        options = polldb.get_options(id)
        for (name, desc) in options:
            if(database.club_book_exists(name, desc) and polldb.book_exists(name, desc, id)):
                print(f"{name}-{desc} already exists")
            elif (database.club_book_exists(name, desc) and not polldb.book_exists(name, desc, id)):
                polldb.sync(id, index, name.title(), desc.title())
                print(f"{name}:{desc} added")
            elif (polldb.book_exists(name, desc, id) and not database.club_book_exists(name, desc)):
                success2 = polldb.remove_polloption(name, desc, id)
                if (success2): print(f"{name}:{desc} removed")
    # if (success):
    #     await update.message.reply_text("Sync'd successfully")
    # else: 
    #     await update.message.reply_text("Cannot sync :( (Possibly added the new options)")
    


async def sendpost(update: Update, querry):
    try:
        url = f"https://app.thestorygraph.com/browse?search_term={querry}"
        async with httpx.AsyncClient() as client:
            page = await client.get(url)
        soup = BeautifulSoup(page.content, 'lxml')
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
        async with httpx.AsyncClient() as client:
            bookpage = await client.get(burl)
        bp = BeautifulSoup(bookpage.content, 'lxml')
        sr = bp.find('span','average-star-rating').text.strip()
        blurb = bp.find('div','blurb-pane').parent.find('script').text
        #print("blurb is :", blurb)
        pattern = re.compile(r"\.html\('([^']*(?:\\.[^']*)*)'\)")
        inht = pattern.search(blurb).group(1)
        #print("after processing :", inht)
        desc = BeautifulSoup(inht,'lxml').text
        star = "⭐"*round(float(sr))
        ser=""
        if seriesname != 'N/A':
            ser = \
f"""
<b><i>{seriesname}</i></b>"""
        
        post = \
f"""\
<b>{bname}</b>{ser}
<i>{aname}</i>
{star} ({sr}/5)

{desc}
"""
        link="<a href='"+burl+"'>Read More...</a>"
        caplen=len(post)
        linklen=len(link)
        if (caplen + linklen) >1024:
            limit = 1024 - linklen -5
            post = post[:limit] + '...\n'
        post+=link
        await update.message.reply_photo(img,post)
    except Exception as e:
        print("error while posting", querry)
        print(e)


async def mkposts(update: Update, context: CallbackContext):
    """Make post with data extracted from goodreads"""
    database = context.bot_data["database"]
    sect = " ".join(context.args).lower() if context.args else None
    sects = ", ".join((Message.MONO.format(TERM=sect) for sect in Literal.SECTIONS))

    if sect in Literal.SECTIONS:
        books = database.list_section(sect)
        querries = (name + " " + auths for (name,auths,users) in books)
        messages = (sendpost(update, querry) for querry in querries)
        await asyncio.gather(*messages)
        await update.message.reply_text("Book posts made successfully!")
    else:
        await update.message.reply_text(
            Message.INVALID_SECTION.format(SECTION=sect, SECTIONS=sects)
        )


async def getbookinfo(update: Update, context: CallbackContext):
    """Get post for any book"""
    bname = " ".join(context.args).lower() if context.args else None

    if bname:
        await sendpost(update, bname)
    else:
        await update.message.reply_text("404 Book Not found")

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

async def days_since (update: Update, context: CallbackContext):
    await update.message.reply_text(f"Days since <b>A Little Life</b> was mentioned: <tg-spoiler>ZERO</tg-spoiler>")
    return await update.message.set_reaction("🗿")

async def haikudetect(update: Update, context: CallbackContext) -> None:
    try:
        if(len(update.message.text) > 1000): 
            await update.message.set_reaction("🔥") 
        if not update.message.text: return
        #reduce frequency of haiku detection
        if update.message.id % 3 != 0: return
        message = update.message.text
        words = message.split()
        # Checking words count
        if (len(words) < 3 or len(words) > 17): return
        # Loading pyphen dictionary
        dic = pyphen.Pyphen(lang=langdetect.detect(message))
        # Counting syllables
        syllable_count_in_message = 0
        syllable_count = 0
        line = 0
        haiku = "<blockquote>"
        for word in words:
            syllable_count += len(dic.inserted(word).split("-"))
            haiku += word + " "
            # First line must have 5 syllables and second 7.
            if ((syllable_count >= 5 and line == 0) or (syllable_count >= 7 and line == 1)): 
                haiku += "\n"
                line += 1
                syllable_count_in_message += syllable_count
                syllable_count = 0
            if (line == 2):
                syllable_count_in_message += syllable_count
                syllable_count = 0
        # Checking for syllables count in message        
        if (syllable_count_in_message < 16 or syllable_count_in_message > 18): return
        # Appending author 
        haiku += f" </blockquote>\n— {update.message.from_user.first_name}"
        # Posting haiku
        await update.message.reply_text("<b>Haiku detected!</b>\n <i>" + haiku + "</i>\n\n#Haiku")
        await update.message.set_reaction("⚡")
    except:
        return
    
async def get_random_quote (update: Update, context: CallbackContext):
    database = context.bot_data["database"]
    print(database)
    authors = database.get_authors()
    authors = [x[0] for x in authors]
    print(authors)
    if(context.args):
        msg = '+'.join(context.args)
    else:
        msg = random.choice(authors)
    print(msg)
    url = f"http://www.goodreads.com/quotes/search?utf8=✓&q={msg}&commit=Search"
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
    finalquote = random.choice(quotes) + '\n\n' + '#Quotes'
    await update.message.reply_text(finalquote)

async def forward_offtopic (update: Update, context: CallbackContext):
    if (not update.message.reply_to_message or not update.message.reply_to_message.text):
        return
    fwd_msg = await context.bot.send_message(Literal.OT_CHAT_ID,f"<a href=\"tg://user?id={update.message.reply_to_message.from_user.id}\">{update.message.reply_to_message.from_user.full_name}</a> said in BookCrushClub:\n\n<blockquote><i>" + update.message.reply_to_message.text + "</i></blockquote>\n\nIt was moved here.\n👇 Please continue below 👇")
    ot_chat_id = str(Literal.OT_CHAT_ID)
    ot_chat_id = ot_chat_id.split("-100",1)
    print(ot_chat_id[1])
    print(fwd_msg.message_id)
    buttons = [
        InlineKeyboardButton(
            text=Label.MOVE_OT,
            url= f"https://t.me/c/{ot_chat_id[1]}/{fwd_msg.message_id}",
        )
    ]
    markup = InlineKeyboardMarkup.from_column(buttons)
    await context.bot.send_message(Literal.BOOKCRUSHCLUB_CHAT_ID, "<b>⚠️ Offtopic alert!</b>\n\n<i>Conversation moved to Offtopic group...</i>", reply_to_message_id = update.message.reply_to_message.id, reply_markup = markup)
    await context.bot.set_message_reaction(Literal.BOOKCRUSHCLUB_CHAT_ID, update.message.reply_to_message.id, "🤨")

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
