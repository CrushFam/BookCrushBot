from telegram import (
    BotCommandScopeAllPrivateChats,
    BotCommandScopeChat,
)
from .constants import Constants


class Scope:

    """
    Represents the various supported command scopes.
    """

    ADMINS = BotCommandScopeChat(Constants.ADMINS_GROUP)
    PRIVATE = BotCommandScopeAllPrivateChats()
