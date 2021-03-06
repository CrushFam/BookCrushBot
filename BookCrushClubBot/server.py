import logging
from telegram.ext import Updater
from .database import Database
from .handlers import handlers


class Server:
    def __init__(self, token: str, database_url: str):

        """
        Server uses Updater to handle different updates from Telegram.
        The bot token and database URL, are obtained from arguments.
        """

        self.updater = Updater(token)
        self.database = Database(database_url)
        self.updater.dispatcher.bot_data["database"] = self.database
        logging.basicConfig(
            format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
        )
        self._add_handlers()

    def _add_handlers(self):

        dispatcher = self.updater.dispatcher
        for handler_type, handles in handlers.items():
            for handler_kwargs, disp_args in handles:
                handler_obj = handler_type(**handler_kwargs)
                dispatcher.add_handler(handler_obj, *disp_args)

    def listen(self, listen: str, port: int, url: str, url_path: str):

        """
        Starts webhook on the URL obtained from environment variable.
        """

        self.updater.start_webhook(
            listen=listen,
            port=port,
            url_path=url_path,
            allowed_updates=["callback_query", "channel_post", "message"],
        )
        self.updater.bot.set_webhook(f"{url}/{url_path}")
        logging.info("Started listening")
        self.updater.idle()

    def poll(self, interval):

        """
        Starts polling for updates.
        """

        self.updater.start_polling(
            allowed_updates=["callback_query", "message"], poll_interval=interval
        )
        logging.info("Started polling")
        self.updater.idle()

    def sig_handler(self, *_):

        """
        Closes the connection to database.
        """

        del self.updater.dispatcher.bot_data["database"]
        logging.info("Shutting down. Bye.")
