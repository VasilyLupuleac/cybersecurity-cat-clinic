from http.server import HTTPServer, BaseHTTPRequestHandler
from passwordStorage import DictPasswordStorage
import os
import cgi


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
        
        elif page == 'register':
            self.send_response(200)
            current_dir = os.path.dirname(os.path.realpath(__file__))
            file_path = os.path.join(current_dir, 'register.html')

            with open(file_path, 'rb') as file:
                html_content = file.read()
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content)
        
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

        elif page == 'register':
            content_type, _ = cgi.parse_header(self.headers['Content-Type'])
            if content_type == 'multipart/form-data':
                form_data = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
                username = form_data.getvalue('username')
                password = form_data.getvalue('password')
                confirm_pwd = form_data.getvalue('confirmPwd')
                print(f'Username: {username}, Password: {password}, Confirm Password: {confirm_pwd}')
            else:
                self.send_response(400)  # Bad request
                self.end_headers()
                self.wfile.write(b'Invalid content type')

        else:
            self.send_response(404)
            self.end_headers()


userStorage = DictPasswordStorage()
PORT = 1642
server = HTTPServer(('localhost', PORT), CustomHTTPRequestHandler)
print(f'Server running on port {PORT}...')
server.serve_forever()
