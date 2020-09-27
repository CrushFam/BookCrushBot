from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)
import BookCrushBot
from .botm_session import BOTMSession
from .review_session import ReviewSession
from .roulette_session import RouletteSession


def send_contact(update, _):

    text = open("data/CONTACT.md").read()
    chat = update.effective_chat
    chat.send_message(text=text, parse_mode="Markdown")


def send_guide(update, _):

    text = open("data/GUIDE.md").read()
    chat = update.effective_chat
    chat.send_message(text=text, parse_mode="Markdown")


def send_help(update, _):

    text = open("data/HELP.md").read()
    chat = update.effective_chat
    chat.send_message(text=text, parse_mode="Markdown")


def send_start(update, _):

    user = update.effective_user
    first = user.first_name if user.first_name else ""
    last = user.last_name if user.last_name else ""
    name = f"{first} {last}"
    botm = "open" if BookCrushBot.BOTM else "closed"
    review = "can" if BookCrushBot.REVIEW else "can not"
    roulette = "accepting" if BookCrushBot.ROULETTE else "not accepting"
    text = open("data/START.md").read().format(NAME=name, BOTM=botm, ROULETTE=roulette)
    chat = update.effective_chat
    chat.send_message(text=text, parse_mode="Markdown")


class Loop:
    def __init__(self):

        self.updater = Updater(
            token=BookCrushBot.TOKEN, use_context=True, user_sig_handler=self.stop
        )
        self.dispatcher = self.updater.dispatcher
        self.sessions = {}

        handlers = [
            ("start", send_start),
            ("contact", send_contact),
            ("guide", send_guide),
            ("help", send_help),
            ("botm", self.start_botm),
            ("review", self.start_review),
            ("roulette", self.start_roulette),
        ]
        message_handler = MessageHandler(Filters.text & (~Filters.command), self.handle_message)
        callback_handler = CallbackQueryHandler(self.handle_query)

        for command, func in handlers:
            handler = CommandHandler(command, func)
            self.dispatcher.add_handler(handler)
        self.dispatcher.add_handler(message_handler)
        self.dispatcher.add_handler(callback_handler)

    def flush_session(self, user_id):

        try:
            session = self.sessions.pop(user_id)
        except KeyError:
            pass
        else:
            session.expire()

    def handle_message(self, update, _):

        if not update.effective_user:
            BookCrushBot.logger.info("Got ping to stay awake")
            return
        user_id = update.effective_user.id
        try:
            session = self.sessions[user_id]
        except KeyError:
            text = "Sorry, I can't get it. Try /help if you are stuck."
            chat = update.effective_chat
            chat.send_message(text=text, parse_mode="Markdown")
        else:
            session.respond_message(update.message)

    def handle_query(self, update, _):

        user_id = update.effective_user.id
        query = update.callback_query
        try:
            session = self.sessions[user_id]
        except KeyError:
            BookCrushBot.logger.warning("Orphan query : %s", query.data)
        else:
            session.respond_query(query)

    def run(self):

        port = BookCrushBot.PORT
        token = BookCrushBot.TOKEN
        BookCrushBot.logger.info("Started server")
        self.updater.start_webhook(listen="0.0.0.0", port=port, url_path=token)
        self.updater.start_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=token,
            allowed_updates=["message", "channel_post", "callback_query"],
        )
        self.updater.bot.set_webhook(f"https://bookcrush-bot.herokuapp.com/{token}")
        self.updater.idle()

    def start_botm(self, update, _):

        user = update.effective_user
        chat = update.effective_chat
        self.flush_session(user.id)

        if BookCrushBot.BOTM:
            session = BOTMSession(chat, user)
            self.sessions[user.id] = session
        else:
            text = "Sorry Book Of The Month suggestions are closed."
            chat.send_message(text=text)

    def start_review(self, update, _):

        user = update.effective_user
        chat = update.effective_chat

        self.flush_session(user.id)

        if BookCrushBot.REVIEW:
            session = ReviewSession(chat, user)
            self.sessions[user.id] = session
        else:
            text = "Sorry, reviews are not accepted now."
            chat.send_message(text=text)

    def start_roulette(self, update, _):

        user = update.effective_user
        chat = update.effective_chat

        self.flush_session(user.id)

        if BookCrushBot.ROULETTE:
            session = RouletteSession(chat, user)
            self.sessions[user.id] = session
        else:
            text = "Sorry Roulette suggestions are closed."
            chat.send_message(text=text)

    def stop(self, *_):

        self.updater.stop()
        BookCrushBot.logger.info("Bye")
