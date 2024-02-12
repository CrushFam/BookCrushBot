"""BookCrushClubBot is a bot to maintain suggestions in the club."""

from os import getenv

from BookCrushClubBot import App

DATABASE_URL = getenv("DATABASE_URL")
POLLBOT_URL = getenv("POLLBOT_URL")
INTERVAL = int(getenv("INTERVAL", 2))
TOKEN = getenv("TOKEN")

app = App(TOKEN, DATABASE_URL, POLLBOT_URL)
app.poll(INTERVAL)
