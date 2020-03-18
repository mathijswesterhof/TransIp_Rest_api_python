from __future__ import annotations
import requests
import json

from HttpLogic.Exceptions import *
from HttpLogic.Authenticate import TransIpAuthenticate


class ApiRequests:

    def __init__(self, auth: TransIpAuthenticate, endpoint: str):
        self.auth = auth
        self.endpoint = endpoint

    def perform_get_request(self, url: str, wrapper):
        """Get data from API."""
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.auth.get_token()}'
        }
        response = requests.get(f'{self.endpoint}{url}', headers=headers)
        content = response.content.decode()
        self._check_status_code(response.status_code, content)

        if response.status_code == 200:
            json_response = json.loads(content)
            return wrapper(json_response)

        raise SystemError('Unexpected status thrown')

    def perform_post_request(self, url: str, data: dict):
        """Get post data from API"""
        if self.auth.read_only:
            raise ReadOnlyTokenError('Cant post request, auth token is read_only')

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.auth.get_token()}'
        }
        response = requests.post(f'{self.endpoint}{url}', data, headers=headers)
        content = response.content.decode()
        self._check_status_code(response.status_code, content)

        if response.status_code != 201:
            raise SystemError('Unexpected status thrown')

    @staticmethod
    def _check_status_code(status_code: int, content: str):
        if status_code == 403:
            raise RestrictedError("Action not allowed.", json.loads(content))

        if status_code == 404:
            raise NotFoundError("Content not found.", json.loads(content))

        if status_code == 406:
            raise NotValidError("Invalid data supplied.", json.loads(content))

        if status_code == 409:
            raise NotEditableError("Not editable data supplied.", json.loads(content))

        if status_code > 499:
            raise ConnectionError(f'5xx error returned by API: {content}')
