import telegram as tgm
import BookCrushBot
from .session import Session


class RouletteSession(Session):
    def __init__(self, bot, chat, user):
        Session.__init__(self, bot, chat, user)
        self.base_message_id = None
        self.books_count = BookCrushBot.get_roulette_additions_count(self.user.id)
        self.books = []
        self.search_results = []
        self.text_message_handler = None
        self.send_welcome()

    def expire(self):

        text = "You have started another session. So this one expired."
        self.bot.edit_message_text(text=text, chat_id=self.chat.id, message_id=self.base_message_id)
        BookCrushBot.DATABASE.commit()

    def get_welcome_message(self):

        parts = [f"*Roulette Portal*\nIdeally there is no limit !"]
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

    def handle_isbn(self, text):

        book = BookCrushBot.get_book_by_isbn(text)
        buttons = [[tgm.InlineKeyboardButton(text="Try again", callback_data="add_isbn"),
                    tgm.InlineKeyboardButton(text="Go Back", callback_data="add")]]

        if book:
            name = book["name"]
            authors = book["authors"]
            text = f"ISBN : {book['isbn']}\n*{name}* by _{authors}_"
            buttons.insert(0, [tgm.InlineKeyboardButton(text="Yes", callback_data="accept_0")])
            self.books = [book]
        else:
            text = "Oops. We can't find a book matching the ISBN."

        keyboard_markup = tgm.InlineKeyboardMarkup(buttons)
        self.bot.edit_message_text(text=text, chat_id=self.chat.id, message_id=self.base_message_id,
                              parse_mode="Markdown", reply_markup=keyboard_markup)

    def handle_name(self, text):

        books = BookCrushBot.get_book_by_name(text)
        url = f"http://openlibrary.org/search?title={text.replace(' ', '+')}"
        buttons = [[tgm.InlineKeyboardButton(text="Try again", callback_data="add_name"),
                    tgm.InlineKeyboardButton(text="Go Back", callback_data="add")]]

        if books:
            parts = [f"We have found the following books."]
            for i, book in enumerate(books):
                name = book["name"]
                authors = book["authors"]
                parts.append(f"{i+1}. ISBN : {book['isbn']}\n*{name}* by _{authors}_\n")
                buttons.insert(i, [tgm.InlineKeyboardButton(text=book["name"], callback_data=f"accept_{i}")])
            parts.append("Not the one you are looking for ?")
            self.books = books
        else:
            parts.append("We can't find a book matching the name.")

        parts.append(f"Please try [narrowing]({url}) your search.")
        text = "\n".join(parts)
        keyboard_markup = tgm.InlineKeyboardMarkup(buttons)
        self.bot.edit_message_text(text=text, chat_id=self.chat.id, message_id=self.base_message_id,
                              parse_mode="Markdown", reply_markup=keyboard_markup, disable_web_page_preview=True)

    def handle_raw(self, text):

        book = BookCrushBot.get_book_by_raw(text)
        buttons = [[tgm.InlineKeyboardButton(text="Try again", callback_data="add_raw"),
                    tgm.InlineKeyboardButton(text="Go Back", callback_data="add")]]

        if book:
            name = book["name"]
            authors = book["authors"]
            text = f"**{name}** by *{authors}*"
            buttons.insert(0, [tgm.InlineKeyboardButton(text="Yes", callback_data="accept_0")])
            self.books = [book]
        else:
            text = "Your message doesn't match the given format. Did you miss something ?"

        keyboard_markup = tgm.InlineKeyboardMarkup(buttons)
        self.bot.edit_message_text(text=text, chat_id=self.chat.id, message_id=self.base_message_id,
                              parse_mode="Markdown", reply_markup=keyboard_markup)

    def handle_search(self, keyword):

        books = BookCrushBot.search_roulette_books(self.user.id, keyword)
        buttons = [[tgm.InlineKeyboardButton(text="Try again", callback_data="remove"),
                    tgm.InlineKeyboardButton(text="Go Back", callback_data="start")]]
        parts = []
        self.search_results = []

        if books:
            parts.append("The following books match the keyword. Choose the book you want to *remove*.")
            parts.append("Please be aware that you *can not undo* the removal.")
            for i, (name, authors) in enumerate(books):
                parts.append(f"{i+1}. *{name}* by _{authors}_")
                buttons.insert(0, [tgm.InlineKeyboardButton(text=name, callback_data=f"remove_{i}")])
                self.search_results.append(name)
            parts.append("Cannot find the book ? Try again with a suitable keyword !")
        else:
            parts.append("Sorry we can't find any book matching the keyword. Why not try again ?")

        text = "\n".join(parts)
        keyboard_markup = tgm.InlineKeyboardMarkup(buttons)
        self.bot.edit_message_text(text=text, chat_id=self.chat.id, message_id=self.base_message_id,
                              parse_mode="Markdown", reply_markup=keyboard_markup)

    def remove_book(self, ix):

        name = self.search_results[ix]
        BookCrushBot.remove_roulette_addition(self.user.id, name)
        self.books_count -= 1

    def respond_message(self, message):

        if self.text_message_handler:
            self.text_message_handler(message["text"])
        else:
            self.bot.send_message_text(chat_id=self.chat.id, text="Please respond by the above buttons.")

    def respond_query(self, query):

        data = query.data
        self.bot.answer_callback_query(callback_query_id=query.id)
        self.text_message_handler = None

        if data == "start":
            self.send_welcome(edit=True)
        elif data == "add":
            self.send_add()
        elif data == "remove":
            self.send_remove()
        elif data.startswith("accept_"):
            ix = int(data.lstrip("accept_"))
            self.submit_book(ix)
            self.send_welcome(edit=True)
        elif data.startswith("remove_"):
            ix = int(data.lstrip("remove_"))
            self.remove_book(ix)
            self.send_welcome(edit=True)
        elif data == "add_isbn":
            self.send_add_by_isbn()
        elif data == "add_name":
            self.send_add_by_name()
        elif data == "add_raw":
            self.send_add_raw()
        else:
            BookCrushBot.logger.warning(f"Unexpected roulette query : {data}")

    def send_add(self):

        text = "Please choose the method of additions."
        buttons = [[tgm.InlineKeyboardButton(text="ISBN",callback_data="add_isbn"),
                    tgm.InlineKeyboardButton(text="Name", callback_data="add_name"),
                    tgm.InlineKeyboardButton(text="Raw", callback_data="add_raw")],
                   [tgm.InlineKeyboardButton(text="Go Back", callback_data="start")]]
        keyboard_markup = tgm.InlineKeyboardMarkup(buttons)
        self.bot.edit_message_text(text=text, chat_id=self.chat.id, message_id=self.base_message_id,
                              reply_markup=keyboard_markup)

    def send_add_by_isbn(self):

        self.text_message_handler = self.handle_isbn
        text = "Enter the ISBN of your book."
        button = tgm.InlineKeyboardButton(text="Go Back", callback_data="add")
        keyboard_markup = tgm.InlineKeyboardMarkup.from_button(button)
        self.bot.edit_message_text(text=text, chat_id=self.chat.id, message_id=self.base_message_id, reply_markup=keyboard_markup)

    def send_add_by_name(self):

        self.text_message_handler = self.handle_name
        text = "Enter the name of your book."
        button = tgm.InlineKeyboardButton(text="Go Back", callback_data="add")
        keyboard_markup = tgm.InlineKeyboardMarkup.from_button(button)
        self.bot.edit_message_text(text=text, chat_id=self.chat.id, message_id=self.base_message_id, reply_markup=keyboard_markup)

    def send_add_raw(self):

        self.text_message_handler = self.handle_raw
        text = "Enter the details of your book in the following format._\nName\nAuthors\nGenres\nNote\n_"
        button = tgm.InlineKeyboardButton(text="Go Back", callback_data="add")
        keyboard_markup = tgm.InlineKeyboardMarkup.from_button(button)
        self.bot.edit_message_text(text=text, chat_id=self.chat.id, message_id=self.base_message_id,
                                   parse_mode="Markdown", reply_markup=keyboard_markup)

    def send_remove(self):

        text = "Enter the name of the book to find and *remove*. Please be aware that you *can not undo* the removal."
        button = tgm.InlineKeyboardButton(text="Go Back", callback_data="start")
        self.text_message_handler = self.handle_search
        keyboard_markup = tgm.InlineKeyboardMarkup.from_button(button)
        self.bot.edit_message_text(text=text, chat_id=self.chat.id, message_id=self.base_message_id,
                              parse_mode="Markdown", reply_markup=keyboard_markup)

    def send_welcome(self, edit=False):

        text, keyboard_markup = self.get_welcome_message()
        if edit:
            self.bot.edit_message_text(text=text, chat_id=self.chat.id, message_id=self.base_message_id,
                                  parse_mode="Markdown", reply_markup=keyboard_markup)
        else:
            message = self.bot.send_message(chat_id=self.chat.id, text=text,
                                            parse_mode="Markdown", reply_markup=keyboard_markup)
            self.base_message_id = message.message_id

    def submit_book(self, ix=0):

        book = self.books[ix]
        BookCrushBot.add_to_roulette(
            self.user.id,
            book["isbn"],
            book["name"],
            book["authors"],
            book["genres"],
            book["note"],
        )
        self.books_count += 1
        self.books = []
