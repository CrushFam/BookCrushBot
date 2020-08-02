import sys
import time
import threading
import BookCrushBot


class Loop:
    def __init__(self, offset=0, sleep=1, journal=sys.stdout, timeout=1):
        self.url = BookCrushBot.URL
        self.data = {
            "allowed_updates": '["message", "callback_query"]',
            "offset": offset,
            "timeout": timeout,
        }
        self.sleep = sleep
        self.sessions = {}
        self.journal = journal

    def handle_updates(self, result):

        for update in result:
            if "message" in update:
                message = update["message"]
                self.respond_message(message)
            elif "callback_query" in update:
                query = update["callback_query"]
                self.respond_query(query)
            else:
                BookCrushBot.log("Mismatching update :", update)

            self.data["offset"] = update["update_id"] + 1

    def respond_message(self, message):

        user_id = message["from"]["id"]
        chat_id = message["chat"]["id"]
        text = message["text"]

        data = {
            "chat_id": chat_id,
            "text": f"_{text}_ \?\?\?\nSorry I did not get it\.",
            "parse_mode": "MarkdownV2",
        }

        if text in ("/contact", "/guide", "/help", "/start"):
            filename = "data/" + text[1:].upper() + ".md"
            msg = open(filename).read()
            data["text"] = msg

            if text == "/start":
                botm = "open" if BookCrushBot.BOTM else "closed"
                roulette = "accepting" if BookCrushBot.ROULETTE else "not accepting"
                start_text = msg.format(USER=message["from"]["first_name"], BOTM=botm, ROULETTE=roulette)
                data["text"] = start_text

            BookCrushBot.request_async(self.url + "/sendMessage", data)

        elif text in ("/botm", "/roulette"):
            try:
                session = self.sessions.pop(user_id)
            except KeyError:
                pass
            else:
                session.expire(premature=True)

            if text == "/botm":
                if BookCrushBot.BOTM:
                    session = BookCrushBot.BOTMSession(message["chat"], message["from"])
                else:
                    data["text"] = "BOTM is closed at the moment\."
                    return BookCrushBot.request_async(self.url + "/sendMessage", data)
            else:
                if BookCrushBot.ROULETTE:
                    session = BookCrushBot.RouletteSession(message["chat"], message["from"])
                else:
                    data["text"] = "Roulette is closed at the moment\."
                    return BookCrushBot.request_async(self.url + "/sendMessage", data)

            self.sessions[chat_id] = session
            BookCrushBot.log(
                f"{text[1:].title()} Session started for {message['from']['username']}"
            )

        else:
            try:
                session = self.sessions[user_id]
            except KeyError:
                BookCrushBot.request_async(self.url + "/sendMessage", data)
            else:
                thread = threading.Thread(
                    target=session.respond_message, args=(message,)
                )
                thread.start()

    def respond_query(self, query):

        user_id = query["from"]["id"]
        try:
            session = self.sessions[user_id]
        except KeyError:
            BookCrushBot.log(f"Orphan query from {query['from']['username']}")
        else:
            thread = threading.Thread(target=session.respond_query, args=(query,))
            thread.start()

    def run(self):

        try:
            self.wait()
        except KeyboardInterrupt:
            self.stop()
            BookCrushBot.log("Bye")

    def stop(self):

        BookCrushBot.DB_CURSOR.close()
        BookCrushBot.DB_CONNECTION.commit()
        BookCrushBot.DB_CONNECTION.close()

    def wait(self):

        while True:
            BookCrushBot.log("Getting updates :", self.data["offset"])
            try:
                result = BookCrushBot.request(self.url + "/getUpdates", self.data)
            except AssertionError as error:
                BookCrushBot.log("Failed to get updates :", error)
            self.handle_updates(result)

            for chat_id, session in tuple(self.sessions.items()):
                if not session.has_time_left():
                    session.expire()
                    self.sessions.pop(chat_id)
            time.sleep(self.sleep)
