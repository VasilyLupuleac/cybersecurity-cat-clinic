import cgi
import os
import ssl
from http.server import HTTPServer, BaseHTTPRequestHandler
from http import cookies

from header_token import make_token, check_token
from passwordStorage import DictPasswordStorage
from dictAppointmentStorage import DictAppointmentStorage


storage = DictPasswordStorage

class CatClinicRequestHandler(BaseHTTPRequestHandler):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.join(current_dir, os.pardir)
    root = os.path.join(parent_dir, os.pardir)
    pages_dir = os.path.join(root, 'cat clinic')

    def send_message(self):
        pass

    def send_html(self, filename):
        file_path = os.path.join(CatClinicRequestHandler.pages_dir, filename)
        with open(file_path, 'rb') as file:
            html = file.read()
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html)

    def check_auth(self):
        cookie_header = self.headers.get('Cookie')
        if not cookie_header:
            return False
        cookie = cookies.SimpleCookie(cookie_header)
        if 'token' not in cookie:
            return False
        token = cookie['token'].value
        return check_token(token)

    def do_GET(self):
        page = self.path.split('/')[1]
        if page == '':
            self.send_response(301)
            self.send_header('Location', '/home')
            self.end_headers()
            return
        if page == 'style.css':
            filename = os.path.join(self.pages_dir, 'style.css')
            with open(filename, 'rb') as file:
                css = file.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            self.wfile.write(css)
            return

        if page == '1.jpg':
            filename = os.path.join(self.pages_dir, '1.jpg')
            with open(filename, 'rb') as file:
                jpg = file.read()
            self.send_response(200)
            self.send_header('Content-type', 'image/jpg')
            self.end_headers()
            self.wfile.write(jpg)

        if page == 'home':
            user = self.check_auth()
            if not user:
                self.send_response(200)
                self.send_html('newusers.html')
                return
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f'Welcome to the clinic, {user}!'.encode('utf-8'))

        elif page == 'login':
            self.send_response(200)
            html_content = self.get_html('login.html')
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content)

        elif page == 'register':
            self.send_response(200)
            self.send_html('register.html')

        elif page == 'book':
            self.send_response(200)
            html_content = self.get_html('bookapp.html')
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content)
        elif page == 'appointments':
            self.send_response(200)
            self.send_html('appointment.html')

        elif page == 'logout':
            cookie_name = 'token'
            invalid_cookie = cookies.SimpleCookie()
            invalid_cookie[cookie_name] = ''
            self.send_response(301)
            self.send_header('Location', '/home')
            self.send_header('Set-Cookie', invalid_cookie.output(header=''))
            self.end_headers()

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        page = self.path.split('/')[1]
        print(f"Received POST request for page: {page}")

        if page == 'login':
            form_data = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
            username = form_data.getvalue('username').strip()
            password = form_data.getvalue('password').strip()
            user_exists = storage.check(username, password)
            if not user_exists:
                self.send_response(403)  # TODO change
                self.end_headers()
                self.send_message('Please check provided information')  # TODO change to HTML page
                return
            token = make_token(username)
            cookie = cookies.SimpleCookie()
            cookie_name = 'token'
            cookie[cookie_name] = token
            cookie[cookie_name]['httponly'] = True
            cookie[cookie_name]['secure'] = True
            self.send_response(200)
            self.send_header('Set-Cookie', cookie.output(header=''))
            self.end_headers()

        elif page == 'register':
            content_type, _ = cgi.parse_header(self.headers['Content-Type'])
            if content_type == 'multipart/form-data':
                form_data = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
                username = form_data.getvalue('username')
                password = form_data.getvalue('password')
                confirm_pwd = form_data.getvalue('confirmPwd')

                print(
                    f"Received registration data - Username: {username}, Password: {password}, Confirm Password: {confirm_pwd}")

                if str(password) == str(confirm_pwd):
                    # TODO adding user to the password storage and checking if the user already exist
                    if storage.add(username, password):
                        self.send_response(201)  # Created (redirect)
                        self.send_header('Location', '/login')  # Redirect to login page
                        self.end_headers()
                    else:
                        self.send_response(200)  # TODO
                        self.send_message('User already exists')
                        self.end_headers()
            else:
                self.send_response(400)  # Bad request
                self.end_headers()
                self.wfile.write(b'Invalid content type')

        elif page == 'book':
            user = self.check_auth()
            if not user:
                self.send_response(401)
                self.end_headers()
                return

            # TODO
            self.end_headers()

        else:
            self.send_response(404)
            self.end_headers()


class CatClinicServer:
    def __init__(self, host, port):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        parent_dir = os.path.join(current_dir, os.pardir)
        root = os.path.join(parent_dir, os.pardir)
        self.pages_dir = os.path.join(root, 'cat clinic')
        self.host = host
        self.port = port

    def run(self):
        server = HTTPServer((self.host, self.port), CatClinicRequestHandler)
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        with open('pass.txt', 'r') as pass_file:
            password = pass_file.readline().strip()
        context.load_cert_chain(keyfile='key.pem',
                                certfile='cert.pem',
                                password=password)
        context.check_hostname = False

        server.socket = context.wrap_socket(server.socket, server_side=True)
        print(f'Server running on port {self.port}...')
        server.serve_forever()


if __name__ == '__main__':
    storage = DictPasswordStorage()
    appointmentStorage = DictAppointmentStorage()
    port = 1642
    host = 'localhost'
    cat_server = CatClinicServer(host, port)
    cat_server.run()
