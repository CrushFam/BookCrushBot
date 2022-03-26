"""Commands available to bot."""

from telegram import BotCommandScopeAllPrivateChats, BotCommandScopeChat

from BookCrushClubBot.constants import Literal

admin = [
    ("broadcast", "Broadcast the message across users"),
    ("clear", "Clear the books of a section"),
    ("get", "Get the value of a key"),
    ("list", "List the books of a section"),
    ("set", "Set the value of a key"),
]

common = [
    ("help", "Help on usage"),
    ("start", "Start the adventure"),
]

member = [
    ("books", "Manage suggestions"),
]

commands = {
    BotCommandScopeChat(Literal.ADMINS_CHAT_ID): admin + common,
    BotCommandScopeAllPrivateChats(): common + member,
}
