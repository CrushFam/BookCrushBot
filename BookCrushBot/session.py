import time
import BookCrushBot


class Session:
    def __init__(self, chat, user, time_limit):

        self.chat_id = chat["id"]
        self.user_id = user["id"]
        self.url = BookCrushBot.URL
        self.time_limit = time_limit
        self.start = time.time()

    def expire(self, premature=False):

        pass

    def has_time_left(self):

        return (time.time() - self.start) < self.time_limit

    def respond_message(self, message):

        pass

    def respond_query(self, query):

        pass
