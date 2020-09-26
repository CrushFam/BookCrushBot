import telegram as tgm
from .functions import (
    add_to_roulette,
    get_roulette_additions_count,
    remove_roulette_addition,
    search_roulette_books,
)
from .session import Session


class RouletteSession(Session):
    def __init__(self, chat, user):
        Session.__init__(self, chat, user)
        self.books_count = get_roulette_additions_count(self.user.id)
        self.search_results = []
        self.send_welcome()

    def get_welcome_message(self):

        parts = ["*Roulette Portal*\nIdeally there is no limit !"]
        ln = self.books_count
        buttons = [tgm.InlineKeyboardButton(text="Add A Book", callback_data="add")]

        if ln == 0:
            parts.append("You have not added any book. Isn't this the perfect moment ?")
        else:
            parts.append(f"You have added {ln} book{'s' * (ln != 1)}.")
            buttons.append(tgm.InlineKeyboardButton(text="Remove Additions", callback_data="remove"))

        text = "\n".join(parts)
        keyboard_markup = tgm.InlineKeyboardMarkup.from_row(buttons)
        return text, keyboard_markup

    def handle_search(self, keyword):

        books = search_roulette_books(self.user.id, keyword)
        buttons = [
            [
                tgm.InlineKeyboardButton(text="Try again", callback_data="remove"),
                tgm.InlineKeyboardButton(text="Go Back", callback_data="start"),
            ]
        ]
        parts = []
        self.search_results = []

        if books:
            parts.append(
                "The following books match the keyword. Choose the book you want to *remove*."
            )
            parts.append("Please be aware that you *can not undo* the removal.")
            for i, (name, authors) in enumerate(books):
                parts.append(f"{i+1}. *{name}* by _{authors}_")
                buttons.insert(
                    0, [tgm.InlineKeyboardButton(text=name, callback_data=f"remove_{i}")],
                )
                self.search_results.append(name)
            parts.append("Cannot find the book ? Try again with a suitable keyword !")
        else:
            parts.append("Sorry we can't find any book matching the keyword. Why not try again ?")

        text = "\n".join(parts)
        keyboard_markup = tgm.InlineKeyboardMarkup(buttons)
        self.base_message.edit_text(text=text, parse_mode="Markdown", reply_markup=keyboard_markup)

    def remove_book(self, ix):

        name = self.search_results[ix]
        remove_roulette_addition(self.user.id, name)
        self.books_count -= 1
        self.send_welcome()

    def respond_message(self, message):

        if self.text_message_handler:
            self.text_message_handler(message["text"])
        else:
            self.chat.send_message_text(text="Please respond by the above buttons.")

    def send_remove(self):

        text = "Enter the name of the book to find and *remove*. Please be aware that you *can not undo* the removal."
        button = tgm.InlineKeyboardButton(text="Go Back", callback_data="start")
        self.text_message_handler = self.handle_search
        keyboard_markup = tgm.InlineKeyboardMarkup.from_button(button)
        self.base_message.edit_text(text=text, parse_mode="Markdown", reply_markup=keyboard_markup)

    def send_welcome(self, edit=False):

        text, keyboard_markup = self.get_welcome_message()
        if edit:
            self.base_message.edit_text(
                text=text, parse_mode="Markdown", reply_markup=keyboard_markup
            )
        else:
            message = self.chat.send_message(
                text=text, parse_mode="Markdown", reply_markup=keyboard_markup
            )
            self.base_message = message

    def submit_book(self, ix=0):

        username = self.user.username if self.user.username else ""
        firstname = self.user.first_name if self.user.first_name else ""
        lastname = self.user.last_name if self.user.last_name else ""
        display_name = f"{firstname} {lastname}"
        book = self.books[ix]
        add_to_roulette(
            self.user.id,
            username,
            display_name,
            book["isbn"],
            book["name"],
            book["authors"],
            book["genres"],
            book["note"],
        )
        self.books_count += 1
        self.books = []
        self.send_welcome()
