import requests
import json
import datetime
import hashlib

from cc_connector import cc_connector_base, ConnectionStatus


class cc_connector_http(cc_connector_base):
    server_url = None
    http_session = None
    handling_request_callback = False


    def __init__(self, server_url, username, password):
        self.server_url = server_url
        self.username = username
        self.password = password
        self.connection_status = ConnectionStatus.DISCONNECTED

    def connect(self):
        if self.connection_status != ConnectionStatus.DISCONNECTED:
            raise(ValueError("Already connected to " + self.server_url))

        self.http_session = requests.Session()

        datas = {'username':self.username, 'password':self.password}

        r = self.http_session.post(self.server_url + 'login.php', data = datas)

