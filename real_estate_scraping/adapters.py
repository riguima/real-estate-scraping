import re
import json
from datetime import date
from selenium.webdriver import Firefox
from selenium.common.exceptions import TimeoutException
from time import sleep

from real_estate_scraping.domain import IBrowser, RealEstate
from real_estate_scraping.validators import valid_real_estate, valid_city, valid_negotiation_type
from real_estate_scraping.use_cases import create_driver
from real_estate_scraping.helpers import find_element, find_elements


class ZapImoveisBrowser(IBrowser):

    def __init__(self, driver: Firefox = None) -> None:
        self._driver = create_driver() if driver is None else driver

    def __del__(self) -> None:
        self._driver.close()

    def search(self, city: str, real_estate_type: str, negotiation_type: str) -> None:
        self._driver.get('https://www.zapimoveis.com.br/')
        if negotiation_type == 'Aluguel':
            element = find_element(self._driver, '.l-tabs__nav-item:nth-child(2)')
            self._driver.execute_script('arguments[0].click();', element)
        states_names = json.load(open('states_names.json', 'r'))
        state = list(states_names.keys())[
            list(states_names.values()).index(city.split(' - ')[-1])
        ]
        find_element(self._driver, '.l-input__input--variant-large').send_keys(
            f'{city.split(" - ")[0]} - {state}')
        element = find_element(self._driver, '.l-checkbox__input')
        self._driver.execute_script('arguments[0].click();', element)
        element = find_element(self._driver, '.l-button--fluid')
        self._driver.execute_script('arguments[0].click();', element)
        for e, element in enumerate(find_elements(self._driver, '.l-checkbox__label')):
            if element.text == real_estate_type:
                find_elements(self._driver, '.l-checkbox__input')[e]
                self._driver.execute_script('arguments[0].click();', element)
        element = find_element(self._driver, '.l-button[type=submit]')
        self._driver.execute_script('arguments[0].click();', element)

    def create_real_estates(self) -> list[RealEstate]:
        result = []
        #search_url = self._driver.current_url
        for c in range(len(find_elements(self._driver, '.simple-card__box'))):
            element = find_element(self._driver, f'.simple-card__box:nth-child({c + 1})')
            #element.click()
            self._driver.execute_script('arguments[0].click();', element)
            #find_element(self._driver, '.info__business-type')
            #result.append(self.create_real_estate_from_page(self._driver.current_url))
            #self._driver.get(search_url)
        return result

    def create_real_estate_from_page(self, url: str) -> RealEstate:
        self._driver.get(url)
        real_estate = RealEstate(
            negotiation_type=self._get_negotiation_type(),
            type=self._get_real_estate_type(),
            city=self._get_city(),
            address=self._get_address(),
            area=self._get_from_feature_item(1),
            bedrooms=self._get_from_feature_item(2),
            car_spaces=self._get_from_feature_item(3),
            bathrooms=self._get_from_feature_item(4),
            advertiser_name=self._get_advertiser_name(),
            phone_number=self._get_phone_number(),
            ad_url=url,
            publication_date=date(2023, 1, 1),
            price=self._get_price(),
        )
        valid_real_estate(real_estate)
        return real_estate

    def _get_negotiation_type(self) -> str:
        return 'Venda' if 'comprar' in find_element(self._driver, '.info__business-type').text else 'Aluguel'

    def _get_real_estate_type(self) -> str:
        return find_element(self._driver, '.info__business-type').text.title().split()[0]

    def _get_city(self) -> str:
        regex = re.compile(r'\w+, (\w+) - (\w{2})$')
        result = regex.findall(find_element(self._driver, '.map__address').text)
        states = json.load(open('states_names.json', 'r'))
        return f'{result[0][0]} - {states[result[0][1]]}'

    def _get_address(self) -> str:
        regex = re.compile(r'(.+),', re.DOTALL)
        return regex.findall(find_element(
            self._driver, '.map__address'
        ).text)[0].replace(',', '').replace(' -', ',')

    def _get_from_feature_item(self, item: int) -> int:
        regex = re.compile(r'(\d+) .+')
        text = find_element(self._driver, f'.feature__container .feature__item:nth-child({item}) span:nth-child(2)').text
        return int(regex.findall(text)[0])

    def _get_advertiser_name(self) -> str:
        self._show_phone_number()
        return find_element(self._driver, '.publisher__title').text

    def _get_phone_number(self) -> int:
        self._show_phone_number()
        regex = re.compile(r'\((\d{2})\) (\d+)-(\d+)')
        return int(''.join(regex.findall(find_element(
            self._driver, '.publisher__phone').text)[0]))

    def _show_phone_number(self) -> None:
        try:
            if '.publisher__phone' not in self._driver.page_source:
                button = find_element(self._driver, '.lead-phone--open__button')
                self._driver.execute_script('arguments[0].click();', button)
        except TimeoutException:
            self._show_phone_number()

    def _get_price(self) -> float:
        return float(find_element(
            self._driver, '.price__item--main strong'
        ).text[3:].replace('.', '').replace(',', '.'))
