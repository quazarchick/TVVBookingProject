import requests
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from core.schemas.booking_schema import BOOKING_SCHEMA
from core.settings.environments import Environment
import allure
from core.clients.endpoints import Endpoints
from core.settings.environments import Environment
from core.settings.config import Users
from core.settings.config import Timeouts
import jsonschema



load_dotenv()

class APIClient:
    def __init__(self):
        environment_str = os.getenv('ENVIRONMENT')
        try:
            environment = Environment[environment_str]
        except KeyError:
            raise ValueError(f"Unsupported environment value: {environment_str}")

        self.base_url = self.get_base_url(environment)
        self.session = requests.Session()
        self.session.headers = {
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

    def ping(self):
        with allure.step("Ping api client"):
            url = f"{self.base_url}{Endpoints.PING_ENDPOINT.value}"
            response = self.session.get(url)
            response.raise_for_status()
        with allure.step("Assert status-code"):
            assert response.status_code == 201, f"Expected status 201 but got {response.status_code}"
        return response.status_code

    def auth(self):
        with allure.step("Getting authentificate"):
            url = f'{self.base_url}{Endpoints.AUTH_ENDPOINT.value}'
            payload = {"username": Users.USERNAME.value, "password": Users.PASSWORD.value}
            response = self.session.post(url, json=payload, timeout=Timeouts.TIMEOUT.value)
            response.raise_for_status()
        with allure.step("Checking status code"):
            assert response.status_code == 200, f"Expected status 200 but got{response.status_code}"
        token = response.json().get('token')
        with allure.step("Updating header with autorization"):
            self.session.headers.update({"Autorization": f"Bearer {token}"})

    def get_booking_by_id(self, booking_id):
        with allure.step("Get booking by ID"):
            url = f'{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{booking_id}'
            response = self.session.get(url)
            response.raise_for_status()
        with allure.step("Check status-code and request body"):
            assert response.status_code == 200, f"Expected status 200 but got{response.status_code}"
            assert jsonschema.validate(response.json(), BOOKING_SCHEMA), f"The received response body does not match the json schema"
        return response.json()

    def delete_booking(self, booking_id):
        with allure.step("Delete Booking"):
            url = f'{self.base_url}/{Endpoints.BOOKING_ENDPOINT.value}/{booking_id}'
            response = self.session.delete(url, auth=HTTPBasicAuth(Users.USERNAME, Users.PASSWORD))
            response.raise_for_status()
        with allure.step("Checking status code"):
            assert response.status_code == 201, f"Expected status 201 but got{response.status_code}"
        return response.status_code == 201

    def create_booking(self, booking_data):
        with allure.step("Create Booking"):
            url = f'{self.base_url}{Endpoints.BOOKING_ENDPOINT}'
            response = self.session.post(url, json=booking_data)
            response.raise_for_status()
        with allure.step("Cheking status code"):
            assert response.status_code == 200, f"Expected status 200 but got{response.status_code}"
        return response.json()

    def get_booking_ids(self, params=None):
        with allure.step("Getting object with booking"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT}"
            response = self.session.get(url, params=params)
            response.raise_for_status()
        with allure.step("Checking status code"):
            assert response.status_code == 200, f"Expected status 200 but got{response.status_code}"
        return response.json()

    def update_booking(self, booking_id, booking_data):
        with allure.step("Update Booking"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT}/{booking_id}"
            response = self.session.put(url, booking_data)
            response.raise_for_status()
        with allure.step("Checking status code"):
            assert response.status_code == 200, f"Expected status 200 but got{response.status_code}"
        return response.json()

    def partial_update_booking(self, booking_id, booking_data):
        with allure.step("Partial Update Booking"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT}/{booking_id}"
            response = self.session.patch(url, booking_data, auth=HTTPBasicAuth(Users.USERNAME, Users.PASSWORD))
            response.raise_for_status()
        with allure.step("Checking status code"):
            assert response.status_code == 200, f"Expected status 200 but got{response.status_code}"
        return response.json()

