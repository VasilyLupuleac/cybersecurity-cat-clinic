import cgi
import os
import ssl
from http.server import HTTPServer, BaseHTTPRequestHandler

from passwordStorage import DictPasswordStorage
from catClinicRequestHandler import CatClinicRequestHandler

access_rights = {'admin': ['home'],
                 'user': ['home']}  # TODO add more


class CatClinicServer:
    def __init__(self, host, port, userStorage):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        parent_dir = os.path.join(current_dir, os.pardir)
        root = os.path.join(parent_dir, os.pardir)
        self.pages_dir = os.path.join(root, 'cat clinic')
        self.userStorage = userStorage
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
    userStorage = DictPasswordStorage()
    port = 1642
    host = 'localhost'
    cat_server = CatClinicServer(host, port, userStorage)
    cat_server.run()
