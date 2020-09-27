import telegram as tgm
import BookCrushBot
from .functions import (
    get_book_by_isbn,
    get_book_by_name,
    get_book_by_raw,
)


class Session:
    def __init__(self, chat: tgm.Chat, user: tgm.User):

        self.chat = chat
        self.user = user
        self.base_message: tgm.Message = None
        self.books = []
        self.text_message_handler = None

    def expire(self, keep_text=True):

        if keep_text and self.base_message.reply_markup:
            self.base_message.edit_reply_markup(reply_markup=None)
        else:
            text = "You have started another session. So this one expired."
            self.base_message.edit_text(text=text)
        BookCrushBot.DATABASE.commit()

    def get_welcome_message(self):

        pass

    def handle_isbn(self, text):

        book = get_book_by_isbn(text)
        buttons = [
            [
                tgm.InlineKeyboardButton(text="Try again", callback_data="suggest_isbn"),
                tgm.InlineKeyboardButton(text="Go Back", callback_data="suggest"),
            ]
        ]

        if book:
            name = book["name"]
            authors = book["authors"]
            text = f"ISBN : {book['isbn']}\n*{name}* by _{authors}_"
            buttons.insert(0, [tgm.InlineKeyboardButton(text="Yes", callback_data="accept_0")])
            self.books = [book]
        else:
            text = "Oops. We can't find a book matching the ISBN."

        keyboard_markup = tgm.InlineKeyboardMarkup(buttons)
        self.base_message.edit_text(text=text, parse_mode="HTML", reply_markup=keyboard_markup)

    def handle_name(self, text):

        books = get_book_by_name(text)
        url = f"http://openlibrary.org/search?title={text.replace(' ', '+')}"
        buttons = [
            [
                tgm.InlineKeyboardButton(text="Try again", callback_data="suggest_name"),
                tgm.InlineKeyboardButton(text="Go Back", callback_data="suggest"),
            ]
        ]

        parts = []
        if books:
            parts.append(r"We have found the following books\.")
            for i, book in enumerate(books):
                name = book["name"]
                authors = book["authors"]
                parts.append(f"{i+1}. ISBN : {book['isbn']}\n*{name}* by _{authors}_\n")
                buttons.insert(
                    i, [tgm.InlineKeyboardButton(text=book["name"], callback_data=f"accept_{i}")],
                )
            parts.append("Not the one you are looking for ?")
            self.books = books
        else:
            parts.append("We can't find a book matching the name.")

        parts.append(f"That's not what you want ? Try [narrowing]({url}) your search.")
        text = "\n".join(parts)
        keyboard_markup = tgm.InlineKeyboardMarkup(buttons)
        self.base_message.edit_text(
            text=text,
            parse_mode="HTML",
            reply_markup=keyboard_markup,
            disable_web_page_preview=True,
        )

    def handle_raw(self, text):

        book = get_book_by_raw(text)
        buttons = [
            [
                tgm.InlineKeyboardButton(text="Try again", callback_data="suggest_raw"),
                tgm.InlineKeyboardButton(text="Go Back", callback_data="suggest"),
            ]
        ]

        if book:
            name = book["name"]
            authors = book["authors"]
            text = f"**{name}** by *{authors}*"
            buttons.insert(0, [tgm.InlineKeyboardButton(text="Yes", callback_data="accept_0")])
            self.books = [book]
        else:
            text = "Your message doesn't match the given format. Did you miss something ?"

        keyboard_markup = tgm.InlineKeyboardMarkup(buttons)
        self.base_message.edit_text(text=text, parse_mode="HTML", reply_markup=keyboard_markup)

    def remove_book(self, ix):

        pass

    def respond_message(self, message: tgm.Message):

        if self.text_message_handler:
            self.text_message_handler(message.text)
        else:
            self.chat.send_message(text="Please respond by above buttons.")

    def respond_query(self, query: tgm.CallbackQuery):

        data = query.data
        query.answer()
        self.text_message_handler = None

        if data == "start":
            self.send_welcome()
        elif data == "suggest":
            self.send_suggest()
        elif data == "remove":
            self.send_remove()
        elif data.startswith("accept_"):
            ix = int(data.lstrip("accept_"))
            self.submit_book(ix)
        elif data.startswith("remove_"):
            ix = int(data.lstrip("remove_"))
            self.remove_book(ix)
        elif data == "suggest_isbn":
            self.send_suggest_by_isbn()
        elif data == "suggest_name":
            self.send_suggest_by_name()
        elif data == "suggest_raw":
            self.send_suggest_raw()
        else:
            BookCrushBot.logger.warning("Unexpected query : %s", data)

    def send_remove(self):

        pass

    def send_suggest(self):

        text = "Please choose the method of suggestion."
        buttons = [
            [
                tgm.InlineKeyboardButton(text="ISBN", callback_data="suggest_isbn"),
                tgm.InlineKeyboardButton(text="Name", callback_data="suggest_name"),
                tgm.InlineKeyboardButton(text="Raw", callback_data="suggest_raw"),
            ],
            [tgm.InlineKeyboardButton(text="Go Back", callback_data="start")],
        ]
        keyboard_markup = tgm.InlineKeyboardMarkup(buttons)
        self.base_message.edit_text(text=text, reply_markup=keyboard_markup)

    def send_suggest_by_isbn(self):

        self.text_message_handler = self.handle_isbn
        text = "Enter the ISBN of your book."
        button = tgm.InlineKeyboardButton(text="Go Back", callback_data="suggest")
        keyboard_markup = tgm.InlineKeyboardMarkup.from_button(button)
        self.base_message.edit_text(text=text, reply_markup=keyboard_markup)

    def send_suggest_by_name(self):

        self.text_message_handler = self.handle_name
        text = "Enter the name of your book."
        button = tgm.InlineKeyboardButton(text="Go Back", callback_data="suggest")
        keyboard_markup = tgm.InlineKeyboardMarkup.from_button(button)
        self.base_message.edit_text(text=text, reply_markup=keyboard_markup)

    def send_suggest_raw(self):

        self.text_message_handler = self.handle_raw
        text = "Enter the details of your book in the following format._\nName\nAuthors\nGenres\nNote\n_"
        button = tgm.InlineKeyboardButton(text="Go Back", callback_data="suggest")
        keyboard_markup = tgm.InlineKeyboardMarkup.from_button(button)
        self.base_message.edit_text(text=text, parse_mode="HTML", reply_markup=keyboard_markup)

    def send_welcome(self, edit=True):

        text, keyboard_markup = self.get_welcome_message()
        if edit:
            self.base_message.edit_text(
                text=text, parse_mode="HTML", reply_markup=keyboard_markup
            )
        else:
            message = self.chat.send_message(
                text=text, parse_mode="HTML", reply_markup=keyboard_markup,
            )
            self.base_message = message

    def submit_book(self, ix):

        pass
