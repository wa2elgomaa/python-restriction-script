from requests import request
import json


class Requester:
    def __init__(self , env_config):
        self.env_config = env_config
        self.headers = {
            'Authorization': f'Bearer {self.env_config.get("TOKEN")}',
            'Content-Type': 'application/json'
        }

    def fetch(self, url, payload=None):
        try:
            if payload is None:
                payload = {}
            response_api = request('GET', url, headers=self.headers, data=payload)
            if response_api.status_code == 200:
                response = json.loads(response_api.text)
                return response
            else:
                return {'error': response_api.reason}
        except Exception as e:
            raise e

    def put(self, url, payload=None):
        try:
            if payload is None:
                payload = {}
            response_api = request('PUT', url, headers=self.headers, data=json.dumps(payload))
            if response_api.status_code == 200:
                response = json.loads(response_api.text)
            else:
                return {'error': response_api.reason}
            return response
        except Exception as e:
            raise e
