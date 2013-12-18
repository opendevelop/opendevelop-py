import os
import requests

class OpenDevelop(object):
    host = os.getenv('OPENDEVELOP_HOST')
    client_id = os.getenv('OPENDEVELOP_CLIENT_ID')
    client_secret = os.getenv('OPENDEVELOP_CLIENT_SECRET')

    def __init__(self, host=None, client_id=None, client_secret=None):
        if (host):
            self.host = host
        if (client_id):
            self.client_id = client_id
        if (client_secret):
            self.client_secret = client_secret
