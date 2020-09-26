import telegram as tgm
from .functions import add_to_reviews
from .session import Session


class ReviewSession(Session):
    def __init__(self, chat, user):

        Session.__init__(self, chat, user)
        self.book = None
        self.send_welcome(edit=False)

    def get_welcome_message(self):

        text = (
            "Did you read a new book ? Share with us what you feel what about it !\n"
            "First choose your book and then you can write the review."
        )

        buttons = [
            [
                tgm.InlineKeyboardButton(text="ISBN", callback_data="suggest_isbn"),
                tgm.InlineKeyboardButton(text="Name", callback_data="suggest_name"),
                tgm.InlineKeyboardButton(text="Raw", callback_data="suggest_raw"),
            ],
            [tgm.InlineKeyboardButton(text="Go Back", callback_data="start")],
        ]
        keyboard_markup = tgm.InlineKeyboardMarkup(buttons)

        return text, keyboard_markup

    def handle_review(self, review):

        review_ = review.strip()

        if len(review_.split()) < 12:
            text = "That was too short. Add something extra. Use the <i>story writing</i> trick we use in exam !"
            self.text_message_handler = self.handle_review
        else:
            username = self.user.username if self.user.username else ""
            firstname = self.user.first_name if self.user.first_name else ""
            lastname = self.user.last_name if self.user.last_name else ""
            display_name = f"{firstname} {lastname}"
            add_to_reviews(
                self.user.id,
                username,
                display_name,
                self.book["isbn"],
                self.book["name"],
                self.book["authors"],
                self.book["genres"],
                self.book["note"],
                review_,
            )
            text = "Thanks for the review. If you want, you can review more !"

        button = tgm.InlineKeyboardButton(text="Back", callback_data="start")
        keyboard_markup = tgm.InlineKeyboardMarkup.from_button(button)
        self.expire()
        self.chat.send_message(text=text, reply_markup=keyboard_markup, parse_mode="HTML")

    def submit_book(self, ix=0):

        self.book = self.books[ix]
        self.text_message_handler = self.handle_review
        text = (
            "Awesome. Now tell me how the book was ?\n"
            "Protip from Gold Fish of Qeden : A short and sweet review catches eye of the reader.\n"
        )
        button = tgm.InlineKeyboardButton(text="Back", callback_data="start")
        keyboard_markup = tgm.InlineKeyboardMarkup.from_button(button)
        self.base_message.edit_text(text=text, reply_markup=keyboard_markup, parse_mode="HTML")
