import allure
import jsonschema
import pytest
import requests
from core.schemas.booking_schema import BOOKING_SCHEMA


@allure.feature("Test CreateBooking")
@allure.story("Test Create booking")
def test_create_booking(api_client):
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
    jsonschema.validate(response, BOOKING_SCHEMA)