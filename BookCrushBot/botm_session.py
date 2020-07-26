import BookCrushBot
from .session import Session


class BOTMSession(Session):

    def __init__(self, chat, user, time_limit=300):
        Session.__init__(self, chat, user, time_limit)
        self.base_message_id = None
        self.books = []
        self.suggested_books = BookCrushBot.get_botm_suggestions(self.user_id)
        self.text_message_handler = None
        self.send_welcome()

    def expire(self, premature=False):

        if premature:
            message = "You have started another session. So this one expired."
        else:
            message = "Sorry, your session expired. Use /botm to start a new session."

        data = {"chat_id": self.chat_id,
                "text": message,
                "message_id": self.base_message_id}
        try:
            BookCrushBot.request_async(self.url + "/editMessageText", data)
        except AssertionError:
            return f"Failed to expire session of {self.base_message['from']['username']}"

    def get_welcome_message(self):

        text = f"*Book Of The Month Portal*\nYou can suggest {BookCrushBot.BOTM_LIMIT} books\.\n"
        ln = len(self.suggested_books)
        books = enumerate(self.suggested_books)

        if ln == 0:
            text += "You have not suggested any book\. Let's get started now \!\n"
            buttons = [("Suggest A Book", "botm_suggest")]
        else:
            text += "You have suggested the following books :\n"
            text += "\n".join((f"  {i+1}\. _{BookCrushBot.escape(name)}_" for (i, name) in books))
            text += "\n"

            if ln < BookCrushBot.BOTM_LIMIT:
                more = BookCrushBot.BOTM_LIMIT - ln
                text += f"{more} more book{'s' * (more != 1)} can be added \!"
                buttons = [("Suggest A Book", "botm_suggest"), ("Remove Suggested", "botm_remove")]
            else:
                text += "To add more books, you need to remove the suggested ones \.\.\."
                buttons = [("Remove Suggested", "botm_remove")]

        keyboard_markup = BookCrushBot.get_buttons_markup([buttons])

        data = {"chat_id": self.chat_id,
                "text": text,
                "parse_mode": "MarkdownV2",
                "reply_markup": keyboard_markup}

        return data

    def handle_isbn(self, text):

        book = BookCrushBot.get_book_by_isbn(text)
        buttons = [[("Try again", "botm_suggest_isbn"), ("Go Back", "botm_suggest")]]

        if book:
            name = BookCrushBot.escape(book["name"])
            author = BookCrushBot.escape(book["author"])

            message_text = f"ISBN : {book['isbn']}\n*{name}* by _{author}_"
            buttons.insert(0, [("Yes", "botm_accept_0")])
            self.books = [book]

        else:
            message_text = "Oops\. We can't find a book matching the ISBN\."

        keyboard_markup = BookCrushBot.get_buttons_markup(buttons)

        data = {"chat_id": self.chat_id,
                "message_id": self.base_message_id,
                "text": message_text,
                "parse_mode": "MarkdownV2",
                "reply_markup": keyboard_markup}

        BookCrushBot.request(self.url + "/editMessageText", data)

    def handle_name(self, text):

        books = BookCrushBot.get_book_by_name(text)
        url = f"http://openlibrary.org/search?title={text.replace(' ', '+')}"
        buttons = [[("Try again", "botm_suggest_name"), ("Go Back", "botm_suggest")]]

        if books:
            message_text = f"We have found the following books\.\n"

            for i, book in enumerate(books):
                name = BookCrushBot.escape(book["name"])
                author = BookCrushBot.escape(book["author"])
                message_text += f"{i+1}\. ISBN : {book['isbn']}\n*{name}* by _{author}_\n\n"
                buttons.insert(i, [(book["name"], f"botm_accept_{i}")])

            message_text += "Not the one you are looking for \?\n"
            self.books = books

        else:
            message_text = "We can't find a book matching the name\."

        message_text += f"Please try [narrowing]({url}) your search\."
        keyboard_markup = BookCrushBot.get_buttons_markup(buttons)

        data = {"chat_id": self.chat_id,
                "message_id": self.base_message_id,
                "text": message_text,
                "parse_mode": "MarkdownV2",
                "reply_markup": keyboard_markup}

        BookCrushBot.request(self.url + "/editMessageText", data)

    def handle_raw(self, text):

        book = BookCrushBot.get_book_by_raw(text)
        buttons = [[("Try again", "botm_suggest_raw"), ("Go Back", "botm_suggest")]]

        if book:
            name = BookCrushBot.escape(book["name"])
            author = BookCrushBot.escape(book["author"])
            message_text = f"**{name}** by *{author}*"
            buttons.insert(0, [("Yes", "botm_accept_0")])
            self.books = [book]

        else:
            message_text = "Your message doesn't match the given format. Did you miss something ?"

        keyboard_markup = BookCrushBot.get_buttons_markup(buttons)

        data = {"chat_id": self.chat_id,
                "message_id": self.base_message_id,
                "text": message_text,
                "parse_mode": "MarkdownV2",
                "reply_markup": keyboard_markup}

        BookCrushBot.request(self.url + "/editMessageText", data)

    def remove_book(self, name):

        BookCrushBot.remove_botm_suggestion(self.user_id, name)
        self.suggested_books.remove(name)

    def respond_message(self, message):

        if self.text_message_handler:
            self.text_message_handler(message["text"])
        else:
            data = {"chat_id": self.chat_id, "text": "Please respond by the above buttons."}
            BookCrushBot.request(self.url + "/sendMessage", data)

    def respond_query(self, query):

        data = query["data"]
        BookCrushBot.request(self.url + "/answerCallbackQuery", {"callback_query_id": query["id"]})
        self.text_message_handler = None

        if data == "botm_start":
            self.send_welcome(edit=True)

        elif data == "botm_suggest":
            self.send_suggest()

        elif data == "botm_remove":
            self.send_remove()

        elif data.startswith("botm_accept_"):
            ix = int(data.lstrip("botm_accept_"))
            self.submit_book(ix)
            self.send_welcome(edit=True)

        elif data.startswith("botm_remove_"):
            name = data.lstrip("botm_remove_")
            self.remove_book(name)
            self.send_welcome(edit=True)

        elif data == "botm_suggest_isbn":
            self.send_suggest_by_isbn()

        elif data == "botm_suggest_name":
            self.send_suggest_by_name()

        elif data == "botm_suggest_raw":
            self.send_suggest_raw()

        else:
            BookCrushBot.log("Unexpected BOTM query :", data)

    def send_remove(self):

        text = "Choose the book you want to *remove*\. Please be aware that you *can not undo* the removal\."
        buttons = [[(name, f"botm_remove_{name}")] for name in self.suggested_books]
        buttons.append([("Go Back", "botm_start")])

        keyboard_markup = BookCrushBot.get_buttons_markup(buttons)

        data = {"chat_id": self.chat_id,
                "message_id": self.base_message_id,
                "text": text,
                "parse_mode": "MarkdownV2",
                "reply_markup": keyboard_markup}

        BookCrushBot.request(self.url + "/editMessageText", data)

    def send_suggest(self):

        text = "Please choose the method of suggestion."
        buttons = [[("ISBN", "botm_suggest_isbn"), ("Name", "botm_suggest_name"), ("Raw", "botm_suggest_raw")],
                   [("Go Back", "botm_start")]]
        keyboard_markup = BookCrushBot.get_buttons_markup(buttons)

        data = {"chat_id": self.chat_id,
                "message_id": self.base_message_id,
                "text": text,
                "reply_markup": keyboard_markup}

        BookCrushBot.request(self.url + "/editMessageText", data)["message_id"]

    def send_suggest_by_isbn(self):

        self.text_message_handler = self.handle_isbn

        text = "Enter the ISBN of your book."
        buttons = [[("Go Back", "botm_suggest")]]
        keyboard_markup = BookCrushBot.get_buttons_markup(buttons)

        data = {"chat_id": self.chat_id,
                "message_id": self.base_message_id,
                "text": text,
                "reply_markup": keyboard_markup}

        BookCrushBot.request(self.url + "/editMessageText", data)

    def send_suggest_by_name(self):

        self.text_message_handler = self.handle_name

        text = "Enter the name of your book."
        buttons = [[("Go Back", "botm_suggest")]]
        keyboard_markup = BookCrushBot.get_buttons_markup(buttons)

        data = {"chat_id": self.chat_id,
                "message_id": self.base_message_id,
                "text": text,
                "reply_markup": keyboard_markup}

        BookCrushBot.request(self.url + "/editMessageText", data)

    def send_suggest_raw(self):

        self.text_message_handler = self.handle_raw

        text = "Enter the details of your book in the following format\._\nName\nAuthor\nGenre A\nGenre B\nNote\n_"

        buttons = [[("Go Back", "botm_suggest")]]
        keyboard_markup = BookCrushBot.get_buttons_markup(buttons)

        data = {"chat_id": self.chat_id,
                "message_id": self.base_message_id,
                "text": text,
                "parse_mode": "MarkdownV2",
                "reply_markup": keyboard_markup}

        BookCrushBot.request(self.url + "/editMessageText", data)

    def send_welcome(self, edit=False):

        data = self.get_welcome_message()
        if edit:
            data["message_id"] = self.base_message_id
            BookCrushBot.request(self.url + "/editMessageText", data)
        else:
            self.base_message_id = BookCrushBot.request(self.url + "/sendMessage", data)["message_id"]

    def submit_book(self, ix=0):

        book = self.books[ix]
        BookCrushBot.add_botm_suggestion(
            self.user_id, book["isbn"], book["name"], book["author"], book["genre_a"], book["genre_b"], book["note"]
            )
        self.suggested_books.append(book["name"])
        self.books = []
