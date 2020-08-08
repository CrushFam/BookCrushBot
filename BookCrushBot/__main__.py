import http.server as server
from threading import Thread
import BookCrushBot


class Handler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200, "OK")
            self.end_headers()


serverd = server.HTTPServer(("", 8000), Handler)
thread = Thread(target=serverd.serve_forever, daemon=True)

print("Starting")
thread.start()

loop = BookCrushBot.Loop()
loop.run()

thread.join()
