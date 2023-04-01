import re
import requests
from datetime import datetime

from real_estate_scraping.domain import RealEstate
from real_estate_scraping.use_cases import get_cities
from real_estate_scraping import exceptions


def valid_real_estate(real_estate: RealEstate) -> None:
    validation_functions = [
        valid_negotiation_type, valid_city, valid_phone_number,
        valid_publication_date, valid_ad_url
    ]
    for f in validation_functions:
        f(real_estate)


def valid_negotiation_type(real_estate: RealEstate) -> None:
    if real_estate.negotiation_type.lower() not in ['venda', 'aluguel']:
        raise exceptions.InvalidNegotiationType(
            'Escolha somente Venda ou Aluguel')


def valid_city(real_estate: RealEstate) -> None:
    if real_estate.city not in get_cities():
        raise exceptions.InvalidCity('Cidade não existe')


def valid_phone_number(real_estate: RealEstate) -> None:
    number_length = len(str(real_estate.phone_number))
    if number_length != 11 and number_length != 10:
        raise exceptions.InvalidPhoneNumber('Numero de telefone inválido')


def valid_publication_date(real_estate: RealEstate) -> None:
    if real_estate.publication_date > datetime.now().date():
        raise exceptions.InvalidPublicationDate(
            'Data de publicação não pode ser uma data futura')


def valid_ad_url(real_estate: RealEstate) -> None:
    regex = re.compile((r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a'
                        r'-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'))
    if not regex.findall(real_estate.ad_url):
        raise exceptions.InvalidAdURL('URL inválida')
    response = requests.get(real_estate.ad_url)
    if response.status_code == 404:
        raise exceptions.InvalidAdURL('Página inexistente')
