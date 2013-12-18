import base64
import json
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
        auth_tuple = (self.client_id, self.client_secret)
        auth_bearer = base64.standard_b64encode('%s:%s' % auth_tuple)
        header_value = 'Basic %s' % auth_bearer
        return header_value

    def request(self, method, resource, payload='', headers={}, files={}):
        url = 'http://%s/api/%s' % (self.host, resource)
        response = requests.request(method, url, data=payload, headers=headers,
                                    files=files)
        response.raise_for_status()
        try:
            data = response.json()
        except ValueError:
            data = response.text
        return data

    def authenticated_request(self, method, resource, payload='', headers={},
                              files={}):
        headers['Authorization'] = self._auth_header
        response = self.request(method, resource, payload, headers, files)
        return response

    def images(self):
        return self.request('get', 'images')

    def create_sandbox(self, image, cmd, file_list=[]):
        if (type(cmd) == list):
            cmd = json.dumps(cmd)
        payload = {
            'image': image,
            'cmd': cmd
        }
        files = {}
        for f in file_list:
            if (not (type(f) == str)):
                raise Exception('File should be absolute path in string format')
            if (not os.path.exists(f)):
                raise Exception('File %s does not exist.' % f)
            file_name = os.path.basename(f)
            files[file_name] = (file_name, open(f, 'rb'))
        return self.authenticated_request('post', 'sandbox', payload=payload,
                                          files=files)

    def sandbox(self, sandbox_slug):
        resource = 'sandbox/%s' % sandbox_slug
        return self.authenticated_request('get', resource)
