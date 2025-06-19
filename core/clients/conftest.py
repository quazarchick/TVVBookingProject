import requests
import pytest

BASE_URL = {'https://restful-booker.herokuapp.com/'}

@pytest.fixture(scope="function")
def create_booking():
    payload = {
        "firstname" : "Jim",
        "lastname" : "Brown",
        "totalprice" : 111,
        "depositpaid" : True,
        "bookingdates" : {
            "checkin" : "2018-01-01",
            "checkout" : "2019-01-01"
        },
        "additionalneeds" : "Breakfast"
    }
    response = requests.post(url=f"{BASE_URL}/booking", json=payload)
    assert response.status_code == 200
    return response.json()