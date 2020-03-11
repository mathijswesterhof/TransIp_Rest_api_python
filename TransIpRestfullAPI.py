import json
import os
import re
import requests
import base64
from OpenSSL import crypto


class TransIpRestfulAPI:

    login = ''
    private_key = None
    endpoint = 'api.transip.nl'
    version = 'v6'
    read_only = True
    global_key = False
    expiration_time = '30 minutes'
    label = 'scanner_token'
    signature = None

    def __init__(self, login: str, key_url: str):
        """Set Api with credentials."""

        self.login = login
        self._set_private_key(key_url)
        self.token = None

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

    def set_global_key(self, global_key: bool):
        """Set restriction on whitelist ip."""
        self.global_key = bool(global_key)

    def create_token(self) -> dict:
        """Create bearing token based on settings."""
        request_body = self._get_request_body()
        self.signature = self._create_signature(request_body)
        response = self._perform_request(request_body)

        if response is None or not response.ok:
            print(json.load(response.content))
            raise RuntimeError(f"An error occurred: {response}")

        self.token = json.load(response.content)

    def get_domains(self):
        """Get a list of owned domains."""
        request = f'https://{self.endpoint}/{self.version}/domains'
        return self._perform_data_get_request(request)

    def get_domain(self, domain: str):
        """Get a specific owned domain."""
        request = f'https://{self.endpoint}/{self.version}/domains/{domain}'
        return self._perform_data_get_request(request)

    def get_dns_records_for_domain(self, domain: str):
        """Get all dns records for specific domain."""
        request = f'https://{self.endpoint}/{self.version}/domains/{domain}/dns'
        return self._perform_data_get_request(request)

    def _set_private_key(self, key_url):
        """Set private key from file."""
        with open(key_url, 'r') as key:
            lines = key.readlines()
            raw_key = ''.join(lines).replace('\n', '')
        matches = re.match('^-{5}BEGIN (RSA )?PRIVATE KEY-{5}(.*)-{5}END (RSA )?PRIVATE KEY-{5}$', raw_key)

        if matches is None:
            raise ValueError('Private key is not valid.')

        base_key = matches.groups()[1].strip().replace(r'\s*', '')
        formatted_key = '\n'.join(base_key[i:min(i + 64, len(base_key))] for i in range(0, len(base_key), 64))
        self.private_key = f"-----BEGIN PRIVATE KEY-----\n{formatted_key}\n-----END PRIVATE KEY-----"

    def _get_auth_url(self) -> str:
        """Generate url based on version."""
        return f'https://{self.endpoint}/{self.version}/auth'

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

    def _perform_request(self, request_body: str) -> requests.Response:
        """Query the endpoint for token."""
        headers = {
            'Content-Type': 'application/json',
            'Signature': self.signature
        }
        response = requests.post(self._get_auth_url(), headers=headers, data=request_body)
        return response

    def _perform_data_get_request(self, url: str):
        if self.token is None:
            self.create_token()

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        response = requests.post(url, headers=headers)
        return response

    def _create_signature(self, parameters) -> str:
        """Generate signature based on settings."""
        key = crypto.load_privatekey(crypto.FILETYPE_PEM, self.private_key, b'')
        return base64.b64encode(crypto.sign(key, parameters.encode('utf-8'), 'SHA512')).decode('utf-8')
