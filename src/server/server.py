import cgi
import os
import ssl
import json
from datetime import datetime
from http import cookies
from http.server import HTTPServer, BaseHTTPRequestHandler

from dictAppointmentStorage import DictAppointmentStorage
from header_token import make_token, check_token
from passwordStorage import DictPasswordStorage

passwordStorage = DictPasswordStorage()
appointmentStorage = DictAppointmentStorage()

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.join(current_dir, os.pardir)
root = os.path.join(parent_dir, os.pardir)
pages_dir = os.path.join(root, 'cat clinic')


class CatClinicRequestHandler(BaseHTTPRequestHandler):
    def send_message(self):
        pass

    def send_html(self, filename):
        file_path = os.path.join(pages_dir, filename)
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
            filename = os.path.join(pages_dir, 'style.css')
            with open(filename, 'rb') as file:
                css = file.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            self.wfile.write(css)
            return
        images = ['1.jpg', 'pusheen_happy.jpg', 'pusheen_mid.jpg', 'pusheen_sad.jpg'] + [f'doctor{i}.jpg' for i in
                                                                                         range(1, 5)]
        if page in images:
            filename = os.path.join(pages_dir, page)
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
            self.send_html('index.html')

        elif page == 'login':
            self.send_response(200)
            self.send_html('login.html')

        elif page == 'register':
            self.send_response(200)
            self.send_html('register.html')

        elif page == 'contact':
            user = self.check_auth()
            if not user:
                self.send_response(200)
                self.send_html('contact_new.html')
                return
            self.send_response(200)
            self.send_html('contact.html')

        elif page == 'book':
            user = self.check_auth()
            if not user:
                self.send_response(401)
                self.end_headers()
                return
            self.send_response(200)
            self.send_html('book.html')

        elif page == 'appointments':
            user = self.check_auth()
            if not user:
                self.send_response(401)
                self.end_headers()
                return
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
            user_exists = passwordStorage.check(username, password)
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

                if str(password) == str(confirm_pwd):
                    if passwordStorage.add(username, password):
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

            form_data = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
            print(form_data.keys())
            doctor = form_data.getvalue('doctor') or form_data.getvalue('Doctors')
            print(doctor)
            date = datetime.strptime(form_data.getvalue('date'), "%Y-%m-%d").date()

            if not appointmentStorage.check_doctor(doctor):
                self.send_response(400)
                self.end_headers()
                return

            apts = appointmentStorage.get_appointments_day(doctor, date)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(apts).encode('utf-8'))

        elif page == 'reserve':
            user = self.check_auth()
            if not user:
                self.send_response(401)
                self.end_headers()
                return

            json_string = self.rfile.read(int(self.headers['Content-Length']))
            json_data = json.loads(json_string)
            time = json_data['time']
            date = json_data['date']
            doctor = json_data['doctor']

            if not appointmentStorage.check_doctor(doctor):
                self.send_response(400)
                self.end_headers()
                return

            success = appointmentStorage.reserve_time(doctor, user, date, time)
            if not success:
                self.send_response(200)
                self.send_message('Selected time is unavailable')
                self.end_headers()
            else:
                self.send_response(201)
                self.send_header('Location', '/home')
                self.end_headers()

        elif page == 'appointments':
            user = self.check_auth()
            if not user:
                self.send_response(401)
                self.end_headers()
                return

            apts = appointmentStorage.get_user_appointments(user)
            apts = [{'date': date, 'time': time, 'doctor': doctor} for date, time, doctor in apts]
            apts_json = json.dumps(apts)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(apts_json.encode(encoding='utf_8'))

        else:
            self.send_response(404)
            self.end_headers()


class CatClinicServer:
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        keyfile = os.path.join(root, 'key.pem')
        certfile = os.path.join(root, 'cert.pem')
        self.context.load_cert_chain(keyfile=keyfile,
                                  certfile=certfile,
                                  password=password)
        self.context.check_hostname = False

    def run(self):
        server = HTTPServer((self.host, self.port), CatClinicRequestHandler)
        server.socket = self.context.wrap_socket(server.socket, server_side=True)
        print(f'Server running at https://{self.host}:{self.port}')
        server.serve_forever()


if __name__ == '__main__':
    passwordStorage = DictPasswordStorage()
    appointmentStorage = DictAppointmentStorage()
    port = 1642
    host = 'localhost'
    cat_server = CatClinicServer(host, port, 'Kitten')
    cat_server.run()
