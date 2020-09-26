import telegram


class Session:
    def __init__(self, chat: telegram.Chat, user: telegram.User):

        self.chat = chat
        self.user = user

    def expire(self, keep_text=True):

        pass

    def respond_message(self, message: telegram.Message):

        pass

    def respond_query(self, query: telegram.CallbackQuery):

        pass
