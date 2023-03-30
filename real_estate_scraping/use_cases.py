import geonamescache
import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import pandas as pd

from real_estate_scraping.domain import RealEstate
from real_estate_scraping import exceptions


def create_driver() -> webdriver.Firefox:
    options = Options()
    options.add_argument('-headless')
    return webdriver.Firefox(options=options, service=Service(GeckoDriverManager().install()))


def get_cities() -> list[str]:
    gc = geonamescache.GeonamesCache()
    result = []
    for city in gc.get_cities().values():
        data = json.load(open('states.json', 'r'))
        if city['countrycode'] == 'BR' and city['admin1code'] in data.keys():
            result.append(f'{city["name"]} - {data[city["admin1code"]]}')
    return sorted(result)


def to_excel(real_estates: list[RealEstate], path: str) -> None:
    if path.split('.')[-1] != 'xlsx':
        raise exceptions.ToExcelError('É possivel gerar planilhas apenas com extensão xlsx')
    data = {'Tipo de negociação': [], 'Tipo do imóvel': [],
            'Cidade': [], 'Contato do anunciante': [], 'Nome do anunciante': [],
            'Preço': [], 'Endereço': [], 'Área': [], 'Quartos': [],
            'Banheiros': [], 'Vagas': [], 'Data da publicação': [], 'Link': []}
    for r in real_estates:
        add_real_estate(r, data)
    df = pd.DataFrame(data)
    df.to_excel(path, index=False)


def add_real_estate(real_estate: RealEstate, data: dict) -> None:
    data['Tipo de negociação'].append(real_estate.negotiation_type)
    data['Tipo do imóvel'].append(real_estate.type)
    data['Cidade'].append(real_estate.city)
    data['Contato do anunciante'].append(real_estate.phone_number)
    data['Nome do anunciante'].append(real_estate.advertiser_name)
    data['Preço'].append(real_estate.price)
    data['Endereço'].append(real_estate.address)
    data['Área'].append(real_estate.area)
    data['Quartos'].append(real_estate.bedrooms)
    data['Banheiros'].append(real_estate.bathrooms)
    data['Vagas'].append(real_estate.car_spaces)
    data['Data da publicação'].append(real_estate.publication_date)
    data['Link'].append(real_estate.ad_url)
