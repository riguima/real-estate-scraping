import pytest
from datetime import datetime, timedelta

from real_estate_scraping import validators
from real_estate_scraping import exceptions


def test_negotiation_type_validator(real_estate) -> None:
    validators.valid_negotiation_type(real_estate)
    with pytest.raises(exceptions.InvalidNegotiationType):
        real_estate.negotiation_type = 'Financiar'
        validators.valid_negotiation_type(real_estate)


def test_city_validator(real_estate) -> None:
    validators.valid_city(real_estate)
    with pytest.raises(exceptions.InvalidCity):
        real_estate.city = 'Nao existe'
        validators.valid_city(real_estate)


def test_phone_number_validator(real_estate) -> None:
    validators.valid_phone_number(real_estate)
    with pytest.raises(exceptions.InvalidPhoneNumber):
        real_estate.phone_number = 5511998835264
        validators.valid_phone_number(real_estate)


def test_address_validator(real_estate) -> None:
    validators.valid_address(real_estate)
    with pytest.raises(exceptions.InvalidAddress):
        real_estate.address = 'Rua tal, Nova Monte Serrat 551'
        validators.valid_address(real_estate)


def test_publication_date_validator(real_estate) -> None:
    validators.valid_publication_date(real_estate)
    with pytest.raises(exceptions.InvalidPublicationDate):
        real_estate.publication_date = (datetime.now().date() + timedelta(days=5))
        validators.valid_publication_date(real_estate)


def test_ad_url_validator(real_estate) -> None:
    validators.valid_ad_url(real_estate)
    with pytest.raises(exceptions.InvalidAdURL):
        real_estate.ad_url = 'url invalida'
        validators.valid_ad_url(real_estate)
