import telegram as tgm
import BookCrushBot
from .session import Session


class BOTMSession(Session):
    def __init__(self, bot, chat, user):
        Session.__init__(self, bot, chat, user)
        self.base_message_id = None
        self.books = []
        self.suggested_books = BookCrushBot.get_botm_suggestions(self.user.id)
        self.text_message_handler = None
        self.send_welcome()

    def expire(self):

        text = "You have started another session. So this one expired."
        self.bot.edit_message_text(
            text=text, chat_id=self.chat.id, message_id=self.base_message_id
        )
        BookCrushBot.DATABASE.commit()

    def get_welcome_message(self):

        limit = BookCrushBot.BOTM_LIMIT
        parts = [
            f"*Book Of The Month Portal*\nYou can suggest {limit} book{'s' * (limit != 1)}.\n"
        ]
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
            parts.extend(
                (
                    f"  {i+1}. *{name}*\n   _{authors}_\n"
                    for (i, (name, authors)) in books
                )
            )
            if ln < BookCrushBot.BOTM_LIMIT:
                more = BookCrushBot.BOTM_LIMIT - ln
                parts.append(f"{more} more book{'s' * (more != 1)} can be added !")
            else:
                sug, prnon = (
                    ("suggestion", "it") if ln == 1 else ("suggestions", "them")
                )
                new = "a new book" if limit == 1 else "new books"
                footnote = f"\nIf you'd like to edit your {sug}, you can remove {prnon} and suggest {new} instead."
                parts.append(footnote)
                buttons.pop(0)

        text = "\n".join(parts)
        keyboard_markup = tgm.InlineKeyboardMarkup.from_row(buttons)
        return text, keyboard_markup

    def handle_isbn(self, text):

        book = BookCrushBot.get_book_by_isbn(text)
        buttons = [
            [
                tgm.InlineKeyboardButton(
                    text="Try again", callback_data="suggest_isbn"
                ),
                tgm.InlineKeyboardButton(text="Go Back", callback_data="suggest"),
            ]
        ]

        if book:
            name = book["name"]
            authors = book["authors"]
            text = f"ISBN : {book['isbn']}\n*{name}* by _{authors}_"
            buttons.insert(
                0, [tgm.InlineKeyboardButton(text="Yes", callback_data="accept_0")]
            )
            self.books = [book]
        else:
            text = "Oops. We can't find a book matching the ISBN."

        keyboard_markup = tgm.InlineKeyboardMarkup(buttons)
        self.bot.edit_message_text(
            text=text,
            chat_id=self.chat.id,
            message_id=self.base_message_id,
            parse_mode="Markdown",
            reply_markup=keyboard_markup,
        )

    def handle_name(self, text):

        books = BookCrushBot.get_book_by_name(text)
        url = f"http://openlibrary.org/search?title={text.replace(' ', '+')}"
        buttons = [
            [
                tgm.InlineKeyboardButton(
                    text="Try again", callback_data="suggest_name"
                ),
                tgm.InlineKeyboardButton(text="Go Back", callback_data="suggest"),
            ]
        ]

        parts = []
        if books:
            parts.append(f"We have found the following books\.")
            for i, book in enumerate(books):
                name = book["name"]
                authors = book["authors"]
                parts.append(f"{i+1}. ISBN : {book['isbn']}\n*{name}* by _{authors}_\n")
                buttons.insert(
                    i,
                    [
                        tgm.InlineKeyboardButton(
                            text=book["name"], callback_data=f"accept_{i}"
                        )
                    ],
                )
            parts.append("Not the one you are looking for ?")
            self.books = books
        else:
            parts.append("We can't find a book matching the name.")

        parts.append(f"That's not what you want ? Try [narrowing]({url}) your search.")
        text = "\n".join(parts)
        keyboard_markup = tgm.InlineKeyboardMarkup(buttons)
        self.bot.edit_message_text(
            text=text,
            chat_id=self.chat.id,
            message_id=self.base_message_id,
            parse_mode="Markdown",
            reply_markup=keyboard_markup,
            disable_web_page_preview=True,
        )

    def handle_raw(self, text):

        book = BookCrushBot.get_book_by_raw(text)
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
            buttons.insert(
                0, [tgm.InlineKeyboardButton(text="Yes", callback_data="accept_0")]
            )
            self.books = [book]
        else:
            text = (
                "Your message doesn't match the given format. Did you miss something ?"
            )

        keyboard_markup = tgm.InlineKeyboardMarkup(buttons)
        self.bot.edit_message_text(
            text=text,
            chat_id=self.chat.id,
            message_id=self.base_message_id,
            parse_mode="Markdown",
            reply_markup=keyboard_markup,
        )

    def remove_book(self, ix=0):

        (name, _) = self.suggested_books.pop(ix)
        BookCrushBot.remove_botm_suggestion(self.user.id, name)

    def respond_message(self, message):

        if self.text_message_handler:
            self.text_message_handler(message.text)
        else:
            self.bot.send_message(
                chat_id=self.chat.id, text="Please respond by above buttons."
            )

    def respond_query(self, query):

        data = query.data
        self.bot.answer_callback_query(callback_query_id=query.id)
        self.text_message_handler = None

        if data == "start":
            self.send_welcome(edit=True)
        elif data == "suggest":
            self.send_suggest()
        elif data == "remove":
            self.send_remove()
        elif data.startswith("accept_"):
            ix = int(data.lstrip("accept_"))
            self.submit_book(ix)
            self.send_welcome()
        elif data.startswith("remove_"):
            ix = int(data.lstrip("remove_"))
            self.remove_book(ix)
            self.send_welcome()
        elif data == "suggest_isbn":
            self.send_suggest_by_isbn()
        elif data == "suggest_name":
            self.send_suggest_by_name()
        elif data == "suggest_raw":
            self.send_suggest_raw()
        else:
            BookCrushBot.logger.warning(f"Unexpected BOTM query : {data}")

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
        self.bot.edit_message_text(
            text=text,
            chat_id=self.chat.id,
            message_id=self.base_message_id,
            parse_mode="Markdown",
            reply_markup=keyboard_markup,
        )

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
        self.bot.edit_message_text(
            text=text,
            chat_id=self.chat.id,
            message_id=self.base_message_id,
            reply_markup=keyboard_markup,
        )

    def send_suggest_by_isbn(self):

        self.text_message_handler = self.handle_isbn
        text = "Enter the ISBN of your book."
        button = tgm.InlineKeyboardButton(text="Go Back", callback_data="suggest")
        keyboard_markup = tgm.InlineKeyboardMarkup.from_button(button)
        self.bot.edit_message_text(
            text=text,
            chat_id=self.chat.id,
            message_id=self.base_message_id,
            reply_markup=keyboard_markup,
        )

    def send_suggest_by_name(self):

        self.text_message_handler = self.handle_name
        text = "Enter the name of your book."
        button = tgm.InlineKeyboardButton(text="Go Back", callback_data="suggest")
        keyboard_markup = tgm.InlineKeyboardMarkup.from_button(button)
        self.bot.edit_message_text(
            text=text,
            chat_id=self.chat.id,
            message_id=self.base_message_id,
            reply_markup=keyboard_markup,
        )

    def send_suggest_raw(self):

        self.text_message_handler = self.handle_raw
        text = "Enter the details of your book in the following format._\nName\nAuthors\nGenres\nNote\n_"
        button = tgm.InlineKeyboardButton(text="Go Back", callback_data="suggest")
        keyboard_markup = tgm.InlineKeyboardMarkup.from_button(button)
        self.bot.edit_message_text(
            text=text,
            chat_id=self.chat.id,
            message_id=self.base_message_id,
            parse_mode="Markdown",
            reply_markup=keyboard_markup,
        )

    def send_welcome(self, edit=False):

        text, keyboard_markup = self.get_welcome_message()
        if edit:
            self.bot.edit_message_text(
                text=text,
                chat_id=self.chat.id,
                message_id=self.base_message_id,
                parse_mode="Markdown",
                reply_markup=keyboard_markup,
            )
        else:
            message = self.bot.send_message(
                chat_id=self.chat.id,
                text=text,
                parse_mode="Markdown",
                reply_markup=keyboard_markup,
            )
            self.base_message_id = message.message_id

    def submit_book(self, ix=0):

        username = self.user.username if self.user.username else "-"
        firstname = self.user.first_name if self.user.first_name else "-"
        lastname = self.user.last_name if self.user.last_name else "-"
        display_name = f"{firstname} {lastname}"
        book = self.books[ix]
        BookCrushBot.add_botm_suggestion(
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
