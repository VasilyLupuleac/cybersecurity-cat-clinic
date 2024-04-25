import os
from http.server import BaseHTTPRequestHandler
from header_token import make_token, check_token
import cgi


class CatClinicRequestHandler(BaseHTTPRequestHandler):

    current_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.join(current_dir, os.pardir)
    root = os.path.join(parent_dir, os.pardir)
    pages_dir = os.path.join(root, 'cat clinic')

    def get_html(self, filename):
        file_path = os.path.join(CatClinicRequestHandler.pages_dir, filename)
        with open(file_path, 'rb') as file:
            html = file.read()
        return html

    def check_auth(self, page):
        bearer = self.headers.get('Authorization', '')
        if not bearer.startswith('Bearer '):
            return False
        token = bearer[len('Bearer '):]
        result = check_token(token)
        if not result:
            return False
        user, rights = result  # TODO remove rights
        return user

    def do_GET(self):
        page = self.path.split('/')[1]
        if page == 'home':
            result = self.check_auth(page)
            if not result:
                self.send_response(401)
                self.end_headers()
                self.wfile.write(b'Not logged in!')
                return
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f'Welcome to the clinic, {result[0]}!'.encode('utf-8'))

        elif page == 'login':
            self.send_response(200)
            html_content = self.get_html('login.html')
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content)

        elif page == 'register':
            self.send_response(200)
            html_content = self.get_html('register.html')
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content)

        elif page == 'appointment':
            self.send_response(200)
            html_content = self.get_html('appointment.html')
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content)

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
            user_exists = self.userStorage.check(username, password)
            if not user_exists:
                self.send_response(200)  # TODO change
                self.end_headers()
                print('Please check provided information')  # TODO change to HTML page
                return
            token = make_token(username)
            self.send_header('Authorization', f'Bearer {token}')
            self.send_response(200)
            self.end_headers()
            print('Logged in!')  # TODO change

        elif page == 'register':
            content_type, _ = cgi.parse_header(self.headers['Content-Type'])
            print(f"Content-Type: {content_type}")
            if content_type == 'multipart/form-data':
                form_data = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})
                username = form_data.getvalue('username')
                password = form_data.getvalue('password')
                confirm_pwd = form_data.getvalue('confirmPwd')

                print(
                    f"Received registration data - Username: {username}, Password: {password}, Confirm Password: {confirm_pwd}")

                if str(password) == str(confirm_pwd):
                    # TODO adding user to the password storage and checking if the user already exist

                    print("User Added Successfully")

                    # After successful user registration

                    self.send_response(200)  # Found (redirect)
                    self.send_header('Location',
                                     '/register?success=true')  # Redirect to registration page with success query parameter
                    self.end_headers()

                    # else:
                    #    print("User Already exists")

            else:
                self.send_response(400)  # Bad request
                self.end_headers()
                self.wfile.write(b'Invalid content type')

        else:
            self.send_response(404)
            self.end_headers()
