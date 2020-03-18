import json
import os
import re
import requests
import base64

from datetime import datetime
from time import sleep
from OpenSSL import crypto


class TransIpAuthenticate:

    def __init__(self, login: str, key_url: str, endpoint: str):
        """Set Api with credentials and basic settings."""
        self.login = login
        self.endpoint = endpoint
        self.label = 'Python_API_token'
        self.expiration_time = '30 minutes'
        self.read_only = True
        self.global_key = False
        self.token = None
        self._private_key = self._create_private_key(key_url)
        self._init_time = None
        self._signature = None

    def set_label(self, label: str):
        """Set label."""
        self.label = label

    def set_time(self, time: str):
        """Set time."""
        match = re.match('^([0-5]?[0-9] minutes)|([0-9]+ hours)$', time)
        if match is None:
            raise ValueError('set_time accepts `0-59 minutes` or `1+ hours`')

        self.expiration_time = match.groups()[0] if match.groups()[0] is not None else match.groups()[1]

    def set_read_only(self, read_only: bool):
        """Set read status."""
        self.read_only = bool(read_only)
        self.token = None

    def set_global_key(self, global_key: bool):
        """Set restriction on whitelist ip."""
        self.global_key = bool(global_key)
        self.token = None

    def get_token(self) -> dict:
        """Create bearing token based on settings."""
        if self.token is not None and not self._expired():
            return self.token
        if self.token is not None and self._expired():
            sleep(1)  # make sure that the expired token is propagated.

        request_body = self._get_request_body()
        self._init_time = datetime.now()
        self._signature = self._create_signature(self._private_key, request_body)
        response = self._perform_auth_request(request_body)

        if response is None or not response.ok:
            raise RuntimeError(f"An error occurred: {response}")

        response = json.loads(response.content.decode())
        self.token = response['token']
        return response['token']

    def _get_request_body(self) -> str:
        """Get settings as string."""
        return json.dumps({
            'login': self.login,
            'nonce': base64.b64encode(os.urandom(16)).decode('utf-8'),
            'read_only': self.read_only,
            'expiration_time': self.expiration_time,
            'label': self.label,
            'global_key': self.global_key
        }).replace(', ', ',').replace(': ', ':')

    def _perform_auth_request(self, request_body: str) -> requests.Response:
        """Query the endpoint for token."""
        headers = {
            'Content-Type': 'application/json',
            'Signature': self._signature
        }
        response = requests.request(
            'post',
            f'{self.endpoint}/auth',
            headers=headers,
            data=request_body
        )
        return response

    def _expired(self):
        now = datetime.now()
        delta = now - self._init_time
        time = self.expiration_time.split(' ')[0]
        minutes = int(time)*60 if 'hours' in self.expiration_time else int(time)
        return delta.total_seconds() > (minutes * 60) - 1

    @staticmethod
    def _create_private_key(key_url: str) -> str:
        """Get private key from file."""
        with open(key_url, 'r') as key:
            lines = key.readlines()
            raw_key = ''.join(lines).replace('\n', '')

        regex = r'^-{5}BEGIN (RSA )?PRIVATE KEY-{5}(.*)-{5}END (RSA )?PRIVATE KEY-{5}$'
        matches = re.match(regex, raw_key)

        if matches is None:
            raise ValueError('Private key is not valid.')

        base_key = matches.groups()[1].strip().replace(r'\s*', '')
        formatted_key = '\n'.join(
            base_key[i:min(i + 64, len(base_key))]
            for i in range(0, len(base_key), 64)
        )
        return f"-----BEGIN PRIVATE KEY-----\n{formatted_key}\n-----END PRIVATE KEY-----"

    @staticmethod
    def _create_signature(private_key: str, parameters: str) -> str:
        """Generate signature based on key and parameters."""
        key = crypto.load_privatekey(crypto.FILETYPE_PEM, private_key, b'')
        return base64.b64encode(crypto.sign(key, parameters.encode('utf-8'), 'SHA512')).decode('utf-8')
