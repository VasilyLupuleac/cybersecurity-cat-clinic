from http.server import HTTPServer, BaseHTTPRequestHandler


class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        page = self.path.split('/')[1]
        if page == 'home':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Welcome to the clinic!')
        elif page == 'messages':
            self.send_response(403)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        page = self.path.split('/')[1]
        if page == 'login':
            # TODO check login
            # TODO set headers
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Not implemented')
        else:
            self.send_response(404)
            self.end_headers()


PORT = 1642
server = HTTPServer(('localhost', PORT), CustomHTTPRequestHandler)
print(f'Server running on port {PORT}...')
server.serve_forever()

