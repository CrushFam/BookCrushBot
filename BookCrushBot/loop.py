from telegram.ext import CallbackQueryHandler, CommandHandler, Filters, MessageHandler, Updater
import BookCrushBot


class Loop:
    def __init__(self):

        self.updater = Updater(token=BookCrushBot.TOKEN, use_context=True, user_sig_handler=self.stop)
        self.dispatcher = self.updater.dispatcher
        self.sessions = {}

        handlers = [("start", self.send_start), ("contact", self.send_contact),
                    ("guide", self.send_guide), ("help", self.send_help),
                    ("botm", self.start_botm), ("roulette", self.start_roulette)]
        message_handler = MessageHandler(Filters.text & (~Filters.command), self.handle_message)
        callback_handler = CallbackQueryHandler(self.handle_query)

        for command, func in handlers:
            handler = CommandHandler(command, func)
            self.dispatcher.add_handler(handler)
        self.dispatcher.add_handler(message_handler)
        self.dispatcher.add_handler(callback_handler)

    def flush_session(self, user_id):

        try:
            session = self.sessions[user_id]
        except KeyError:
            pass
        else:
            session.expire()

    def handle_message(self, update, context):

        if not update.effective_user:
            BookCrushBot.logger.info("Got ping to stay awake")
            return
        user_id = update.effective_user.id
        try:
            session = self.sessions[user_id]
        except KeyError:
            text = "Sorry, I can't get it. Try /help if you are stuck."
            chat_id = update.effective_chat.id
            context.bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")
        else:
            session.respond_message(update.message)

    def handle_query(self, update, context):

        user_id = update.effective_user.id
        try:
            session = self.sessions[user_id]
        except KeyError:
            BookCrushBot.logger.warning(f"Orphan query : {update.query.data}")
        else:
            session.respond_query(update.callback_query)

    def run(self):

        port = BookCrushBot.PORT
        token = BookCrushBot.TOKEN
        BookCrushBot.logger.info("Started server")
        self.updater.start_webhook(listen="0.0.0.0", port=port, url_path=token, allowed_updates=["message", "channel_post", "callback_query"])
        self.updater.bot.set_webhook(f"https://bookcrush-bot.herokuapp.com/{token}")
        self.updater.idle()

    def send_contact(self, update, context):

        text = open("data/CONTACT.md").read()
        chat_id = update.effective_chat.id
        context.bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")

    def send_guide(self, update, context):

        text = open("data/GUIDE.md").read()
        chat_id = update.effective_chat.id
        context.bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")

    def send_help(self, update, context):

        text = open("data/HELP.md").read()
        chat_id = update.effective_chat.id
        context.bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")

    def send_start(self, update, context):

        user = update.effective_user
        first = user.first_name if user.first_name else ""
        last = user.last_name if user.last_name else ""
        name = f"{first} {last}"
        botm = "open" if BookCrushBot.BOTM else "closed"
        roulette = "accepting" if BookCrushBot.ROULETTE else "not accepting"
        text = open("data/START.md").read().format(NAME=name, BOTM=botm, ROULETTE=roulette)
        chat_id = update.effective_chat.id
        context.bot.send_message(chat_id=chat_id, text=text, parse_mode="Markdown")

    def start_botm(self, update, context):

        user = update.effective_user
        chat = update.effective_chat
        self.flush_session(user.id)

        if BookCrushBot.BOTM:
            session = BookCrushBot.BOTMSession(context.bot, user, chat)
            self.sessions[user.id] = session
        else:
            text = "Sorry Book Of The Month suggestions are closed."
            context.bot.send_message(chat_id=chat.id, text=text)

    def start_roulette(self, update, context):

        user = update.effective_user
        chat = update.effective_chat

        self.flush_session(user.id)

        if BookCrushBot.ROULETTE:
            session = BookCrushBot.RouletteSession(context.bot, user, chat)
            self.sessions[user.id] = session
        else:
            text = "Sorry Roulette suggestions are closed."
            context.bot.send_message(chat_id=chat.id, text=text)

    def stop(self, *_):

        self.updater.stop()
        BookCrushBot.logger.info("Bye")
