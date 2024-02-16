"""Contains App object which obtains the updates and distributes them to handlers."""

import html
import logging
import traceback

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, PicklePersistence, CallbackContext, Defaults, Application
from ptbcontrib.ptb_jobstores.sqlalchemy import PTBSQLAlchemyJobStore

from BookCrushClubBot.commands import commands
from BookCrushClubBot.constants import Literal, Message
from BookCrushClubBot.handlers import handlers
from BookCrushClubBot.utils import Database


async def handle_error(update: Update, context: CallbackContext):
    """Handle the error."""
    error = context.error

    if update.callback_query and isinstance(context.error, KeyError):
        # User clicked old buttons whose values are lost after restart.
        await update.callback_query.message.reply_text(Message.ZOMBIE_QUERY)
    else:
        # Different error, report it to admins.
        await update.effective_message.reply_text(Message.UNKNOWN_ERROR)
        err = type(error)
        details = str(error)
        user = update.effective_user
        trace = html.escape("\n".join(traceback.format_exception_only(err, error)[-5:]))
        msg = Message.REPORT.format(
            ERROR=err.__name__,
            DETAILS=details,
            USER_ID=user.id,
            FULL_NAME=user.full_name,
            TRACEBACK=trace,
        )
        await context.bot.send_message(chat_id=Literal.ADMINS_CHAT_ID, text=msg)


class App:
    """
    App uses Updater to handle different updates from Telegram.
    The bot token, taken as TOKEN and database URL, \
    taken as DATABASE_URL are obtained from environment variables.
    """

    def __init__(self, token: str, database_url: str, pollbot_url: str, bcc_jobs_url: str):
        """
        App uses Application to handle different updates from Telegram.
        The bot token, taken as TOKEN and database URL, \
        taken as DATABASE_URL are obtained from environment variables.
        """

        defaults = Defaults(parse_mode=ParseMode.HTML, quote=True)
        self._application = (
            ApplicationBuilder()
            .token(token)
            # .persistence(PicklePersistence(filepath="persistent_storage.pickle"))
            .defaults(defaults)
            .post_init(self._setup_commands)
            .post_shutdown(self._shutdown)
            .build()
        )
        self._application.job_queue.scheduler.add_jobstore(
            PTBSQLAlchemyJobStore(
                application=self._application,
                url=bcc_jobs_url,
            )
        )
        self.database = Database(database_url)
        self.polldb = Database(pollbot_url)
        self._application.bot_data["database"] = self.database
        self._application.bot_data["polldb"] = self.polldb
        self._setup_handlers()
        # self._add_handlers()

    async def _setup_commands(self, *_):
        for scope, cmds in commands.items():
            await self._application.bot.set_my_commands(commands=cmds, scope=scope)

    def _setup_handlers(self):
        # application = Application.builder().token("TOKEN").build()
        # application.job_queue.scheduler.add_jobstore(
        #     PTBSQLAlchemyJobStore(
        #         application=application,
        #         url="postgresql://pi:raspberrypi@localhost/bccjobs",
        #     )
        # )
        for hdlr_type, hdlr_args_lx in handlers.items():
            for hdlr_args in hdlr_args_lx:
                hdlr = hdlr_type(**hdlr_args)
                self._application.add_handler(hdlr)
        self._application.add_error_handler(handle_error)

    # def _add_handlers(self):
    #     #dispatcher = self.updater.dispatcher
    #     #Job persistence
    #     application = Application.builder().token("TOKEN").build()
    #     application.job_queue.scheduler.add_jobstore(
    #         PTBSQLAlchemyJobStore(
    #             application=application,
    #             host="postgresql://pi:raspberrypi@localhost/bccjobs",
    #         )
    #     )
        # for handler_type, handles in handlers.items():
        #     for handler_kwargs, disp_args in handles:
        #         handler_obj = handler_type(**handler_kwargs)
        #         dispatcher.add_handler(handler_obj, *disp_args)
        # for handler_type, handles in deeplinks.items():
        #     for handler_kwargs, disp_args in handles:
        #         handler_obj = handler_type(**handler_kwargs)
        #         dispatcher.add_handler(handler_obj, *disp_args)

    def poll(self, interval: int):
        """Starts polling for updates."""
        logging.info("Started polling")
        self._application.run_polling(
            poll_interval=interval,
            allowed_updates=Literal.UPDATES,
            drop_pending_updates=True,
        )

    async def _shutdown(self, *_):
        """Closes the connection to database."""
        for db in self._application.user_data.values():
            msg = db.get("baseMessage", None)
            if msg is not None:
                try:
                    await msg.edit_reply_markup()
                except Exception:
                    pass
        logging.info("Shutting down. Bye.")
