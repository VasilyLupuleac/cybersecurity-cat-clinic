from http.server import HTTPServer, BaseHTTPRequestHandler
from passwordStorage import DictPasswordStorage
from urllib.parse import parse_qs
import os


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
        
        elif page == 'register.html':
            self.send_response(200)
            current_dir = os.path.dirname(os.path.realpath(__file__))
            file_path = os.path.join(current_dir, 'register.html')

            with open(file_path,'rb') as file:
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
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = parse_qs(post_data)
            username = params['username'][0]
            password = params['password'][0]
            print(username,"----------------",password)


        else:
            self.send_response(404)
            self.end_headers()

        


userStorage = DictPasswordStorage()
PORT = 1642
server = HTTPServer(('localhost', PORT), CustomHTTPRequestHandler)
print(f'Server running on port {PORT}...')
server.serve_forever()

