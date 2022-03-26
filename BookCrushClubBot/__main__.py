"""BookCrushClubBot is a bot to maintain suggestions in the club."""

from os import getenv

from BookCrushClubBot import Server

DATABASE_URL = getenv("DATABASE_URL")
INTERVAL = int(getenv("INTERVAL", 2))
LISTEN = getenv("LISTEN", "0.0.0.0")
PORT = int(getenv("PORT", 80))
TOKEN = getenv("TOKEN")
URL = getenv("URL")

server = Server(TOKEN, DATABASE_URL)

if URL:
    server.listen(LISTEN, PORT, URL, TOKEN)
else:
    server.poll(INTERVAL)
