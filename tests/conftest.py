import pytest
from datetime import date

from real_estate_scraping.domain import RealEstate


@pytest.fixture(scope='function')
def real_estate() -> RealEstate:
    return RealEstate(
        negotiation_type='Venda',
        type='Casa',
        city='Itupeva - São Paulo',
        phone_number=11998835264,
        advertiser_name='Richard',
        price=500000,
        address='Estrada Municipal Waldomiro Fregnhami 551, Nova Monte Serrat',
        area=50,
        bedrooms=2,
        bathrooms=1,
        car_spaces=0,
        publication_date=date(2023, 3, 5),
        ad_url='https://www.zapimoveis.com.br/imovel/venda-apartamento-2-quartos-mobiliado-pacaembu-itupeva-sp-51m2-id-2621400516/',
    )
