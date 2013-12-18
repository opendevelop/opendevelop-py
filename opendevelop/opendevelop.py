import base64
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

    @property
    def _auth_header(self):
        auth_tuple = (client_id, client_secret)
        auth_bearer = base64.standard_b64encode('%s:%s' % auth_tuple)
        header_value = 'Basic %s' % auth_bearer
        return header_value

    def request(self, method, resource, payload='', headers={}):
        url = 'http://%s/api/%s' % (self.host, resource)
        response = requests.request(method, url, data=payload, headers=headers)
        return response.json()

    def authenticated_request(self, method, resource, payload='', headers={}):
        headers['Authorization'] = self._auth_header
        response = self.request(method, resource, payload, headers)

    def images(self):
        return self.request('get', 'images')

    def create_sandbox(self):
        pass

    def sandbox(self):
        pass

    def sandbox_logs(self):
        pass
