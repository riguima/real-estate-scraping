import pytest

from real_estate_scraping.adapters import ZapImoveisBrowser
from real_estate_scraping.use_cases import generate_spreadsheet


def test_generate_spreadsheet() -> None:
    browser = ZapImoveisBrowser()
    real_estate = browser.get_real_estates_from_page('https://www.zapimoveis.com.br/imovel/venda-apartamento-2-quartos-mobiliado-pacaembu-itupeva-sp-51m2-id-2621400516/')
    generate_spreadsheet([real_estate])
