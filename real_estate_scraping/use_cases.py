import geonamescache
import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import pandas as pd
from pathlib import Path

from real_estate_scraping.domain import RealEstate
from real_estate_scraping import exceptions


def create_driver() -> webdriver.Firefox:
    options = Options()
    options.add_argument('-headless')
    return webdriver.Firefox(options=options,
                             service=Service(GeckoDriverManager().install()))


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
        raise exceptions.ToExcelError(
            'É possivel gerar planilhas apenas com extensão xlsx')
    if Path(path).exists():
        df = pd.read_excel(path)
    else:
        df = pd.DataFrame(columns=[
            'Tipo de negociação', 'Tipo do imóvel', 'Cidade',
            'Contato do anunciante', 'Nome do anunciante', 'Preço', 'Endereço',
            'Área', 'Quartos', 'Banheiros', 'Vagas', 'Data da publicação',
            'Link',
        ])
    for r in real_estates:
        if r.ad_url not in df['Link']:
            add_real_estate(r, df)
    df.to_excel(path, index=False)


def add_real_estate(rs: RealEstate, df: pd.DataFrame) -> None:
    df.loc[len(df)] = [rs.negotiation_type, rs.real_estate_type, rs.city,
                       rs.phone_number, rs.advertiser_name, rs.price,
                       rs.address, rs.area, rs.bedrooms, rs.bathrooms,
                       rs.car_spaces, rs.publication_date, rs.ad_url]
