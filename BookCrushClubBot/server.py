"""Contains Server object which obtains the updates and distributes them to handlers."""

import logging

from telegram import ParseMode
from telegram.ext import Defaults, Updater

from BookCrushClubBot.commands import commands
from BookCrushClubBot.constants import Literal
from BookCrushClubBot.handlers import handlers
from BookCrushClubBot.utils import Database


class Server:
    """
    Server uses Updater to handle different updates from Telegram.
    The bot token, taken as TOKEN and database URL, \
    taken as DATABASE_URL are obtained from environment variables.
    """

    def __init__(self, token: str, database_url: str):
        """
        Server uses Updater to handle different updates from Telegram.
        The bot token, taken as TOKEN and database URL, \
        taken as DATABASE_URL are obtained from environment variables.
        """

        defaults = Defaults(parse_mode=ParseMode.HTML, quote=True)
        self.updater = Updater(
            token=token, defaults=defaults, user_sig_handler=self.sig_handler
        )
        self.database = Database(database_url)
        self.updater.dispatcher.bot_data["database"] = self.database
        self._setup_commands(commands)
        self._setup_handlers(handlers)

    def _setup_commands(self, commands: dict):
        for scope, cmds in commands.items():
            self.updater.bot.set_my_commands(commands=cmds, scope=scope)

    def _setup_handlers(self, handlers: dict):
        disp = self.updater.dispatcher
        for hdlr_type, hdlr_args_lx in handlers.items():
            for hdlr_args in hdlr_args_lx:
                hdlr = hdlr_type(**hdlr_args)
                disp.add_handler(hdlr)

    def listen(self, listen: str, port: int, url: str, path: str):
        """Starts webhook based on given arguments.."""
        self.updater.start_webhook(
            listen=listen,
            port=port,
            url_path=path,
            webhook_url=f"{url}/{path}",
            allowed_updates=Literal.UPDATES,
        )
        logging.info("Started listening")
        self.updater.idle()

    def poll(self, interval: int):
        """Starts polling for updates."""
        self.updater.start_polling(
            poll_interval=interval,
            allowed_updates=Literal.UPDATES,
        )
        logging.info("Started polling")
        self.updater.idle()

    def sig_handler(self, *_):
        """Closes the connection to database."""
        for db in self.updater.dispatcher.user_data.values():
            msg = db.get("baseMessage", None)
            if msg:
                try:
                    msg.edit_reply_markup()
                except Exception:
                    pass
        logging.info("Shutting down. Bye.")
