import pytest
from datetime import datetime, timedelta

from real_estate_scraping import validators
from real_estate_scraping.domain import RealEstate
from real_estate_scraping import exceptions


@pytest.fixture(scope='function')
def real_estate() -> RealEstate:
    return RealEstate(
        negotiation_type='Venda',
        type='Casa',
        city='Itupeva',
        phone_number=11998835264,
        price=500000,
        address='Estrada Municipal Waldomiro Fregnhami 551, Nova Monte Serrat',
        area=50,
        bedrooms=1,
        bathrooms=2,
        car_spaces=0,
        publication_date=datetime.now().date,
        ad_url='https://www.zapimoveis.com.br/imovel/venda-apartamento-2-quartos-mobiliado-pacaembu-itupeva-sp-51m2-id-2621400516/',
    )


def test_negotiation_type_validator(real_estate) -> None:
    validators.valid_negotiation_type(real_estate)
    try:
        real_estate.negotiation_type = 'Financiar'
        validators.valid_negotiation_type(real_estate)
    except exceptions.InvalidNegotiationType:
        assert True


def test_city_validator(real_estate) -> None:
    validators.valid_city(real_estate)
    try:
        real_estate.city = 'Nao existe'
        validators.valid_city(real_estate)
    except exceptions.InvalidCity:
        assert True


def test_phone_number_validator(real_estate) -> None:
    validators.valid_phone_number(real_estate)
    try:
        real_estate.phone_number = 5511998835264
        validators.valid_phone_number(real_estate)
    except exceptions.InvalidPhoneNumber:
        assert True


def test_address_validator(real_estate) -> None:
    validators.valid_address(real_estate)
    try:
        real_estate.address = 'Rua tal, Nova Monte Serrat 551'
        validators.valid_address(real_estate)
    except exceptions.InvalidAddress:
        assert True


def test_publication_date_validator(real_estate) -> None:
    validators.valid_publication_date(real_estate)
    try:
        real_estate.publication_date = (datetime.now().date + timedelta(days=5))
        validators.valid_publication_date(real_estate)
    except exceptions.InvalidPublicationDate:
        assert True


def test_ad_url_validator(real_estate) -> None:
    validators.valid_ad_url(real_estate)
    try:
        real_estate.ad_url = 'url invalida'
        validators.valid_ad_url(real_estate)
    except exceptions.InvalidAdURL:
        assert True
