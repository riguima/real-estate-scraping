import geonamescache
import json
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

from real_estate_scraping.domain import RealEstate


def create_driver() -> Chrome:
    #options = Options()
    #options.add_argument('-headless')
    return Chrome(service=Service(ChromeDriverManager().install()))


def get_cities() -> list[str]:
    #gc = geonamescache.GeonamesCache(min_city_population=500)
    gc = geonamescache.GeonamesCache()
    result = []
    for city in gc.get_cities().values():
        data = json.load(open('states.json', 'r'))
        if city['countrycode'] == 'BR' and city['admin1code'] in data.keys():
            result.append(f'{city["name"]} - {data[city["admin1code"]]}')
    return sorted(result)


def append_to_df(real_estates: list[RealEstate], df: pd.DataFrame) -> None:
    for rs in real_estates:
        df.loc[len(df)] = [
            rs.negotiation_type, rs.real_estate_type, rs.city, rs.phone_number,
            rs.advertiser_name, rs.price, rs.address, rs.area, rs.util_area,
            rs.bedrooms, rs.bathrooms, rs.car_spaces, rs.publication_date,
            rs.ad_url
        ]
    return df
