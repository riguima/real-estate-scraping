import pytest
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

from real_estate_scraping.adapters import ZapImoveisBrowser
from real_estate_scraping.use_cases import to_excel
from real_estate_scraping.helpers import find_element


@pytest.fixture(scope='module')
def browser() -> ZapImoveisBrowser:
    browser = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    return ZapImoveisBrowser(browser)


def test_search(browser: ZapImoveisBrowser) -> None:
    browser.search('Itupeva - São Paulo', 'Casa', 'Aluguel')
    find_element(browser._driver, '.simple-card__box')


def test_to_excel(browser: ZapImoveisBrowser) -> None:
    real_estate = browser.create_real_estate_from_page('https://www.zapimoveis.com.br/imovel/venda-apartamento-2-quartos-mobiliado-pacaembu-itupeva-sp-51m2-id-2621400516/')
    to_excel([real_estate], 'tests/zap_imoveis_result.xlsx')
    df = pd.read_excel('tests/zap_imoveis_result.xlsx')
    assert pd.read_excel('tests/zap_imoveis_expected.xlsx').equals(df)
