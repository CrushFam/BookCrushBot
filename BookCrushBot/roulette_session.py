import BookCrushBot
from .session import Session


class RouletteSession(Session):
    def __init__(self, chat, user, time_limit=300):
        Session.__init__(self, chat, user, time_limit)
        self.base_message_id = None
        self.books_count = BookCrushBot.get_roulette_additions_count(self.user_id)
        self.books = []
        self.search_results = []
        self.text_message_handler = None
        self.send_welcome()

    def expire(self, premature=False):

        if premature:
            message = "You have started another session. So this one expired."
        else:
            message = (
                "Sorry, your session expired. Use /roulette to start a new session."
            )

        data = {
            "chat_id": self.chat_id,
            "text": message,
            "message_id": self.base_message_id,
        }
        try:
            BookCrushBot.request_async(self.url + "/editMessageText", data)
        except AssertionError:
            return (
                f"Failed to expire session of {self.base_message['from']['username']}"
            )

    def get_welcome_message(self):

        text = f"*Roulette Portal*\nIdeally there is no limit \!\n"
        ln = self.books_count
        buttons = [("Add A Book", "roulette_add")]

        if ln == 0:
            text += "You have not added any book\. Isn't this the perfect moment \?\n"
        else:
            text += f"You have added {ln} book{'s' * (ln != 1)}\.\n"
            buttons.append(("Remove Additions", "roulette_remove"))

        keyboard_markup = BookCrushBot.get_buttons_markup([buttons])

        data = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "MarkdownV2",
            "reply_markup": keyboard_markup,
        }

        return data

    def handle_isbn(self, text):

        book = BookCrushBot.get_book_by_isbn(text)
        buttons = [[("Try again", "roulette_add_isbn"), ("Go Back", "roulette_add")]]

        if book:
            name = BookCrushBot.escape(book["name"])
            authors = BookCrushBot.escape(book["authors"])

            message_text = f"ISBN : {book['isbn']}\n*{name}* by _{authors}_"
            buttons.insert(0, [("Yes", "roulette_accept_0")])
            self.books = [book]

        else:
            message_text = "Oops\. We can't find a book matching the ISBN\."

        keyboard_markup = BookCrushBot.get_buttons_markup(buttons)

        data = {
            "chat_id": self.chat_id,
            "message_id": self.base_message_id,
            "text": message_text,
            "parse_mode": "MarkdownV2",
            "reply_markup": keyboard_markup,
        }

        BookCrushBot.request(self.url + "/editMessageText", data)

    def handle_name(self, text):

        books = BookCrushBot.get_book_by_name(text)
        url = f"http://openlibrary.org/search?title={text.replace(' ', '+')}"
        buttons = [[("Try again", "roulette_add_name"), ("Go Back", "roulette_add")]]

        if books:
            message_text = f"We have found the following books\.\n"

            for i, book in enumerate(books):
                name = BookCrushBot.escape(book["name"])
                authors = BookCrushBot.escape(book["authors"])
                message_text += (
                    f"{i+1}\. ISBN : {book['isbn']}\n*{name}* by _{authors}_\n\n"
                )
                buttons.insert(i, [(book["name"], f"roulette_accept_{i}")])

            message_text += "Not the one you are looking for \?\n"
            self.books = books

        else:
            message_text = "We can't find a book matching the name\."

        message_text += f"Please try [narrowing]({url}) your search\."
        keyboard_markup = BookCrushBot.get_buttons_markup(buttons)

        data = {
            "chat_id": self.chat_id,
            "message_id": self.base_message_id,
            "text": message_text,
            "parse_mode": "MarkdownV2",
            "reply_markup": keyboard_markup,
        }

        BookCrushBot.request(self.url + "/editMessageText", data)

    def handle_raw(self, text):

        book = BookCrushBot.get_book_by_raw(text)
        buttons = [[("Try again", "roulette_add_raw"), ("Go Back", "roulette_add")]]

        if book:
            name = BookCrushBot.escape(book["name"])
            authors = BookCrushBot.escape(book["authors"])
            message_text = f"**{name}** by *{authors}*"
            buttons.insert(0, [("Yes", "roulette_accept_0")])
            self.books = [book]

        else:
            message_text = (
                "Your message doesn't match the given format\. Did you miss something \?"
            )

        keyboard_markup = BookCrushBot.get_buttons_markup(buttons)

        data = {
            "chat_id": self.chat_id,
            "message_id": self.base_message_id,
            "text": message_text,
            "parse_mode": "MarkdownV2",
            "reply_markup": keyboard_markup,
        }

        BookCrushBot.request(self.url + "/editMessageText", data)

    def handle_search(self, keyword):

        books = BookCrushBot.search_roulette_books(self.user_id, keyword)
        buttons = [[("Try again", "roulette_remove"), ("Go Back", "roulette_start")]]
        text = []
        self.search_results = []

        if books:
            text.append(
                "The following books match the keyword\. Choose the book you want to *remove*\."
            )
            text.append("Please be aware that you *can not undo* the removal\.")
            for i, book in enumerate(books):
                name = BookCrushBot.escape(book["name"])
                authors = BookCrushBot.escape(book["authors"])
                text.append(f"{i+1}\. *{name}* by _{authors}_")
                buttons.insert(0, [(book["name"], f"roulette_remove_{i}")])
                self.search_results.append(book["name"])
            text.append("Cannot find the book \? Try again with a suitable keyword \!")
        else:
            text.append(
                "Sorry we can't find any book matching the keyword\. Why not try again \?"
            )

        message = "\n".join(text)
        keyboard_markup = BookCrushBot.get_buttons_markup(buttons)

        data = {
            "chat_id": self.chat_id,
            "message_id": self.base_message_id,
            "text": message,
            "parse_mode": "MarkdownV2",
            "reply_markup": keyboard_markup,
        }

        BookCrushBot.request(self.url + "/editMessageText", data)["message_id"]

    def remove_book(self, ix):

        name = self.search_results[ix]
        BookCrushBot.remove_roulette_addition(self.user_id, name)
        self.books_count -= 1

    def respond_message(self, message):

        if self.text_message_handler:
            self.text_message_handler(message["text"])
        else:
            data = {
                "chat_id": self.chat_id,
                "text": "Please respond by the above buttons.",
            }
            BookCrushBot.request(self.url + "/sendMessage", data)

    def respond_query(self, query):

        data = query["data"]
        BookCrushBot.request(
            self.url + "/answerCallbackQuery", {"callback_query_id": query["id"]}
        )
        self.text_message_handler = None

        if data == "roulette_start":
            self.send_welcome(edit=True)

        elif data == "roulette_add":
            self.send_add()

        elif data == "roulette_remove":
            self.send_remove()

        elif data.startswith("roulette_accept_"):
            ix = int(data.lstrip("roulette_accept_"))
            self.submit_book(ix)
            self.send_welcome(edit=True)

        elif data.startswith("roulette_remove_"):
            ix = int(data.lstrip("roulette_remove_"))
            self.remove_book(ix)
            self.send_welcome(edit=True)

        elif data == "roulette_add_isbn":
            self.send_add_by_isbn()

        elif data == "roulette_add_name":
            self.send_add_by_name()

        elif data == "roulette_add_raw":
            self.send_add_raw()

        else:
            BookCrushBot.log("Unexpected roulette query :", data)

    def send_add(self):

        text = "Please choose the method of additions."
        buttons = [
            [
                ("ISBN", "roulette_add_isbn"),
                ("Name", "roulette_add_name"),
                ("Raw", "roulette_add_raw"),
            ],
            [("Go Back", "roulette_start")],
        ]
        keyboard_markup = BookCrushBot.get_buttons_markup(buttons)

        data = {
            "chat_id": self.chat_id,
            "message_id": self.base_message_id,
            "text": text,
            "reply_markup": keyboard_markup,
        }

        BookCrushBot.request(self.url + "/editMessageText", data)["message_id"]

    def send_add_by_isbn(self):

        self.text_message_handler = self.handle_isbn

        text = "Enter the ISBN of your book."
        buttons = [[("Go Back", "roulette_add")]]
        keyboard_markup = BookCrushBot.get_buttons_markup(buttons)

        data = {
            "chat_id": self.chat_id,
            "message_id": self.base_message_id,
            "text": text,
            "reply_markup": keyboard_markup,
        }

        BookCrushBot.request(self.url + "/editMessageText", data)

    def send_add_by_name(self):

        self.text_message_handler = self.handle_name

        text = "Enter the name of your book."
        buttons = [[("Go Back", "roulette_add")]]
        keyboard_markup = BookCrushBot.get_buttons_markup(buttons)

        data = {
            "chat_id": self.chat_id,
            "message_id": self.base_message_id,
            "text": text,
            "reply_markup": keyboard_markup,
        }

        BookCrushBot.request(self.url + "/editMessageText", data)

    def send_add_raw(self):

        self.text_message_handler = self.handle_raw

        text = "Enter the details of your book in the following format\._\nName\nAuthors\nGenres\nNote\n_"

        buttons = [[("Go Back", "roulette_add")]]
        keyboard_markup = BookCrushBot.get_buttons_markup(buttons)

        data = {
            "chat_id": self.chat_id,
            "message_id": self.base_message_id,
            "text": text,
            "parse_mode": "MarkdownV2",
            "reply_markup": keyboard_markup,
        }

        BookCrushBot.request(self.url + "/editMessageText", data)

    def send_remove(self):

        text = "Enter the name of the book to find and *remove*\. Please be aware that you *can not undo* the removal\."
        buttons = [[("Go Back", "roulette_start")]]
        self.text_message_handler = self.handle_search

        keyboard_markup = BookCrushBot.get_buttons_markup(buttons)

        data = {
            "chat_id": self.chat_id,
            "message_id": self.base_message_id,
            "text": text,
            "parse_mode": "MarkdownV2",
            "reply_markup": keyboard_markup,
        }

        BookCrushBot.request(self.url + "/editMessageText", data)

    def send_welcome(self, edit=False):

        data = self.get_welcome_message()
        if edit:
            data["message_id"] = self.base_message_id
            BookCrushBot.request(self.url + "/editMessageText", data)
        else:
            self.base_message_id = BookCrushBot.request(
                self.url + "/sendMessage", data
            )["message_id"]

    def submit_book(self, ix=0):

        book = self.books[ix]
        BookCrushBot.add_to_roulette(
            self.user_id,
            book["isbn"],
            book["name"],
            book["authors"],
            book["genres"],
            book["note"],
        )
        self.books_count += 1
        self.books = []
