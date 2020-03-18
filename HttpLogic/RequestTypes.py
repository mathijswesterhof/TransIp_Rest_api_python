from __future__ import annotations
import requests
import json

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

        if response.ok:
            json_response = json.loads(response.content.decode())
            return wrapper(json_response)

        if 399 < response.status_code <= 499:
            json_response = json.loads(response.content.decode())
            return json_response

        if response.status_code > 499:
            raise ConnectionError(f'5xx error returned by API: {response.content.decode()}')

        return None

    def perform_post_request(self, url: str, data: dict):
        """Get post data from API"""
        if self.auth.read_only:
            return False

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.auth.get_token()}'
        }
        response = requests.post(f'{self.endpoint}{url}', data, headers=headers)
        if response.ok:
            return True
        if response.status_code in [403, 404, 406, 409]:
            return False
        if response.status_code > 499:
            raise ConnectionError(f'5xx error returned by API: {response.content.decode()}')

        return None
