"""
This module holds OpenDevelop, the main class of the package, which acts
as the client to the OpenDevelop service.
"""

import base64
import json
import os
import requests


class OpenDevelop(object):
    """
    The main class of the opendevelop package. It is used to
      1. view the available images
      2. create a sandbox
      3. inspect a sandbox' status
    """
    host = os.getenv('OPENDEVELOP_HOST')
    client_id = os.getenv('OPENDEVELOP_CLIENT_ID')
    client_secret = os.getenv('OPENDEVELOP_CLIENT_SECRET')

    def __init__(self, host=None, client_id=None, client_secret=None):
        """
        Initializes the OpenDevelop client based to the given data. If any of
        the arguments is noe being given, it will take its value from the
        corresponding enviroment variable respectively:
          * OPENDEVELOP_HOST
          * OPENDEVELOP_CLIENT_ID
          * OPENDEVELOP_CLIENT_SECRET
        """
        if (host):
            self.host = host
        if (client_id):
            self.client_id = client_id
        if (client_secret):
            self.client_secret = client_secret

    @property
    def _auth_header(self):
        """
        Returns the Authorization header that has to be set, based on the given
        data.
        """
        auth_tuple = (self.client_id, self.client_secret)
        auth_bearer = base64.standard_b64encode('%s:%s' % auth_tuple)
        header_value = 'Basic %s' % auth_bearer
        return header_value

    def request(self, method, resource, payload='', headers={}, files={}):
        """
        Performs an HTTP request to the OpenDevelop server connected. If the
        HTTP response returns a status code >= 400, then an Exception is being
        raised.
        """
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
        """
        Creates the proper OAuth2 header and delegates the request to
        OpenDevelop.request, with the Authorization header set.
        """
        headers['Authorization'] = self._auth_header
        response = self.request(method, resource, payload, headers, files)
        return response

    def images(self):
        """
        Return a list of available images for the OpenDevelop instance that the
        client is connected to.
        """
        return self.request('get', 'images')

    def create_sandbox(self, image, cmd, files=[], timeout=None):
        """
        Create a sandbox and execute the given commands inside the sandbox.
        If any files given, they should be uploaded to the sandbox' data
        directory.
        """
        if (type(cmd) == list):
            cmd = json.dumps(cmd)
        payload = {
            'image': image,
            'cmd': cmd
        }
        if (timeout):
            payload['timeout'] = timeout
        file_dict = {}
        for f in files:
            if (not (type(f) == str)):
                raise Exception('File should be absolute path in string format')
            if (not os.path.exists(f)):
                raise Exception('File %s does not exist.' % f)
            file_name = os.path.basename(f)
            file_dict[file_name] = (file_name, open(f, 'rb'))
        return self.authenticated_request('post', 'sandbox', payload=payload,
                                          files=file_dict)

    def sandbox(self, sandbox_slug):
        """
        Return information about a sandbox in a Python dict
        """
        resource = 'sandbox/%s' % sandbox_slug
        return self.authenticated_request('get', resource)
