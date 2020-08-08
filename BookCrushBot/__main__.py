import http.server as server
from threading import Thread
import BookCrushBot


class Handler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        print("GET")
        if self.path == "/":
            self.send_response(200, "OK")
            self.end_headers()
    def do_POST(self):
        print("POST")
        print(self.path)
        print(self.requestline)


serverd = server.HTTPServer(("", BookCrushBot.PORT), Handler)
thread = Thread(target=serverd.serve_forever, daemon=True)

print("Starting")
thread.start()

#loop = BookCrushBot.Loop()
#loop.run()

thread.join()
