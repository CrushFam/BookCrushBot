from os import getenv
from ReadingClubBot import Server

token = getenv("TOKEN")
database_url = getenv("DATABASE_URL")
interval = int(getenv("POLL_INTERVAL", 1))
listen = getenv("LISTEN")
port = int(getenv("PORT", 0))
url = getenv("URL")
server = Server(token, database_url)

if url:
    server.listen(listen, port, url, token)
else:
    server.poll(interval)
