from telegram import InlineKeyboardButton


class Button:
    REMOVE = InlineKeyboardButton(text="Remove", callback_data="remove")

    SUGGEST = InlineKeyboardButton(text="Suggest", callback_data="suggest")

    SUGGEST_ISBN = InlineKeyboardButton(text="ISBN", callback_data="isbn")

    SUGGEST_NAME = InlineKeyboardButton(text="Name", callback_data="name")

    SUGGEST_RAW = InlineKeyboardButton(text="Raw", callback_data="raw")
