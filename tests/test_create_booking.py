import allure
import jsonschema
import pytest
import requests
from pydantic import ValidationError

from core.models.booking import BookingResponse
from core.schemas.booking_schema import BOOKING_SCHEMA


@allure.feature("Test CreateBooking")
@allure.story("Positive: creating booking with custom data")
def test_create_booking_with_custom_data(api_client):
    booking_data = {
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
    response = api_client.create_booking(booking_data)

    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed {e}")

    assert response['booking']['firstname'] == booking_data['firstname']
    assert response['booking']['lastname'] == booking_data['lastname']
    assert response['booking']['totalprice'] == booking_data['totalprice']
    assert response['booking']['depositpaid'] == booking_data['depositpaid']
    assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
    assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']
    assert response['booking']['additionalneeds'] == booking_data['additionalneeds']

@allure.feature("Test CreateBooking")
@allure.story("Positive: creating booking with ramdom data")
def test_create_booking_with_custom_data(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data
    response = api_client.create_booking(booking_data)

    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed {e}")

    assert response['booking']['firstname'] == booking_data['firstname']
    assert response['booking']['lastname'] == booking_data['lastname']
    assert response['booking']['totalprice'] == booking_data['totalprice']
    assert response['booking']['depositpaid'] == booking_data['depositpaid']
    assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
    assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']
    assert response['booking']['additionalneeds'] == booking_data['additionalneeds']

@allure.feature("Test CreateBooking")
@allure.story("Negative: creating booking with empty body request")
def test_creating_booking_with_empty_body_request(api_client):
    booking_data = {}

    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        api_client.create_booking(booking_data)

    assert "500" in str(exc_info.value), f'Expected 500 error, got: {exc_info.value}'