from telegram import BotCommand

commands = {
    "admins": [
        BotCommand("announce", "Announce all users"),
        BotCommand("clear", "Clear the database"),
        BotCommand("getfiction", "Get books for fiction"),
        BotCommand("getnonfiction", "Get books for non-fiction"),
        BotCommand("getshortstory", "Get short stories"),
        BotCommand("unblock", "Unblocks the user"),
    ],
    "private": [
        BotCommand("fiction", "Suggest books for fiction"),
        BotCommand("help", "Help on usage"),
        BotCommand("nonfiction", "Suggest books for non-fiction"),
        BotCommand("shortstory", "Suggest stories for short story"),
        BotCommand("start", "Start the adventure"),
    ],
}
