import telegram as tgm
import BookCrushBot
from .functions import (
    add_botm_suggestion,
    get_botm_suggestions,
    remove_botm_suggestion,
)
from .session import Session


class BOTMSession(Session):
    def __init__(self, chat, user):

        Session.__init__(self, chat, user)
        self.suggested_books = get_botm_suggestions(self.user.id)
        self.send_welcome(edit=False)

    def get_welcome_message(self):

        limit = BookCrushBot.BOTM_LIMIT
        parts = [f"*Book Of The Month Portal*\nYou can suggest {limit} book{'s' * (limit != 1)}.\n"]
        ln = len(self.suggested_books)
        books = enumerate(self.suggested_books)
        buttons = [
            tgm.InlineKeyboardButton(text="Suggest A Book", callback_data="suggest"),
            tgm.InlineKeyboardButton(text="Remove Suggested", callback_data="remove"),
        ]

        if ln == 0:
            parts.append("You have not suggested any book. Let's get started now !")
            buttons.pop(1)
        else:
            parts.append(f"You have suggested the following book{'s' * (ln != 1)} :")
            parts.extend((f"  {i+1}. *{name}*\n   _{authors}_\n" for (i, (name, authors)) in books))
            if ln < BookCrushBot.BOTM_LIMIT:
                more = BookCrushBot.BOTM_LIMIT - ln
                parts.append(f"{more} more book{'s' * (more != 1)} can be added !")
            else:
                sug, prnon = ("suggestion", "it") if ln == 1 else ("suggestions", "them")
                new = "a new book" if limit == 1 else "new books"
                footnote = f"\nIf you'd like to edit your {sug}, you can remove {prnon} and suggest {new} instead."
                parts.append(footnote)
                buttons.pop(0)

        text = "\n".join(parts)
        keyboard_markup = tgm.InlineKeyboardMarkup.from_row(buttons)
        return text, keyboard_markup

    def remove_book(self, ix):

        (name, _) = self.suggested_books.pop(ix)
        remove_botm_suggestion(self.user.id, name)
        self.send_welcome()

    def send_remove(self):

        text = "Choose the book you want to *remove*. Please be aware that you *can not undo* the removal."
        buttons = [
            tgm.InlineKeyboardButton(text=name, callback_data=f"remove_{name}")
            for name in self.suggested_books
        ]
        books = enumerate(self.suggested_books)
        buttons = [
            tgm.InlineKeyboardButton(text=name, callback_data=f"remove_{i}")
            for (i, (name, _)) in books
        ]
        buttons.append(tgm.InlineKeyboardButton(text="Go Back", callback_data="start"))
        keyboard_markup = tgm.InlineKeyboardMarkup.from_column(buttons)
        self.base_message.edit_text(text=text, parse_mode="Markdown", reply_markup=keyboard_markup)

    def submit_book(self, ix=0):

        username = self.user.username if self.user.username else ""
        firstname = self.user.first_name if self.user.first_name else ""
        lastname = self.user.last_name if self.user.last_name else ""
        display_name = f"{firstname} {lastname}"
        book = self.books[ix]
        add_botm_suggestion(
            self.user.id,
            username,
            display_name,
            book["isbn"],
            book["name"],
            book["authors"],
            book["genres"],
            book["note"],
        )
        self.suggested_books.append((book["name"], book["authors"]))
        self.books = []
        self.send_welcome()
