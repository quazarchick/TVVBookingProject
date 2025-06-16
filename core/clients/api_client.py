import requests
import os
from dotenv import load_dotenv
from core.settings.environments import Environment

load_dotenv()

class APIClient:
    def __init__(self):
        enviroment_str = os.getenv('Environments')
        try:
            enviroment = Environment[enviroment_str]
        except KeyError:
            raise ValueError(f"Unsupported environment value: {enviroment_str}")

        self.base_url = self.get_base_url(enviroment)
        self.headers = {
            'Content-Type': 'application/json'
        }

    def get_base_url(self, enviroment: Environment) -> str:
        if enviroment == Environment.TEST:
            return os.getenv('TEST_BASE_URL')
        elif enviroment == Environment.PROD:
            return os.getenv('PROD_BASE_URL')
        else:
            raise ValueError(f"Unsupported environment")

    def get(self, endpoint, params=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.get(url, headers=self.headers, params=params)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def post(self, endpoint, data=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.post(url, headers=self.headers, json=data)
        if status_code:
            assert response.status_code == status_code
        return response.json()