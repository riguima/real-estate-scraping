import re
from selenium.webdriver import Chrome
from selenium.common.exceptions import TimeoutException
import zapimoveis_scraper as zap
from slugify import slugify
import pandas as pd
from time import sleep

from real_estate_scraping.domain import IBrowser, RealEstate, SearchInfo
from real_estate_scraping.validators import valid_real_estate
from real_estate_scraping.use_cases import create_driver
from real_estate_scraping.helpers import find_element, find_elements


class ZapImoveisBrowser(IBrowser):

    def __init__(self, driver: Chrome = None) -> None:
        self._driver = create_driver() if driver is None else driver

    def __del__(self) -> None:
        self._driver.quit()

    def create_real_estates(self, search_info: SearchInfo,
                            dataframe: pd.DataFrame) -> list[RealEstate]:
        result = []
        real_estates = zap.search(
            localization=(f'{search_info.state.lower()}+'
                          f'{slugify(search_info.city)}'),
            num_pages=search_info.num_pages, acao=search_info.negotiation_type.lower(),
            tipo=search_info.real_estate_type.lower(),
        )
        for rs in real_estates:
            ad_url = f'https://www.zapimoveis.com.br{rs.link}'
            if ad_url not in dataframe['Link']:
                phone_number, advertiser_name = self._get_contact_info(ad_url)
                real_estate = RealEstate(
                    negotiation_type=search_info.negotiation_type.lower(),
                    real_estate_type=search_info.real_estate_type.lower(),
                    city=f'{search_info.city} - {search_info.state}',
                    phone_number=phone_number,
                    price=float(rs.price),
                    address=rs.address,
                    area=int(rs.total_area_m2),
                    bedrooms=int(rs.bedrooms),
                    bathrooms=int(rs.bathrooms),
                    car_spaces=int(rs.vacancies),
                    ad_url=ad_url,
                    advertiser_name=advertiser_name,
                )
                valid_real_estate(real_estate)
                result.append(real_estate)
        return result

    def _get_contact_info(self, url: str) -> None:
        self._driver.get(url)
        result = []
        try:
            button = find_element(
                self._driver,
                ('button.new-l-button.new-l-button--appearance-standard.new-l-'
                 'button--context-primary.new-l-button--size-regular.new-l-but'
                 'ton--icon-left.lead-modal-cta__actions--lead.js-send-message'
                 )
            )
            self._driver.execute_script('arguments[0].click();', button)
            button = find_element(self._driver, '.js-phone-link')
        except TimeoutException:
            button = find_element(self._driver, '.lead-phone--open__button')
        self._driver.execute_script('arguments[0].click();', button)
        regex = re.compile(r'\((\d{2})\) (\d+)-(\d+)')
        result.append(int(''.join(regex.findall(
            find_element(self._driver, '.publisher__phone').text
        )[0])))
        result.append(find_element(
            self._driver, '.publisher__title'
        ).get_attribute('textContent'))
        return result


class ImovelWebBrowser(IBrowser):

    def __init__(self, driver: Chrome = None) -> None:
        self._driver = create_driver() if driver is None else driver

    def __del__(self) -> None:
        self._driver.quit()

    def create_real_estates(self, search_info: SearchInfo,
                            dataframe: pd.DataFrame) -> list[RealEstate]:
        url = ('https://www.imovelweb.com.br/'
               f'{search_info.real_estate_type}-'
               f'{search_info.negotiation_type}-{slugify(search_info.city)}-'
               f'{search_info.state}.html')
        self._driver.get(url.lower())
        result = []
        for p in range(search_info.num_pages):
            for i in range(20):
                try:
                    ad_container = find_elements(self._driver, '.sc-i1odl-2')[i]
                except IndexError:
                    break
                neighborhood = find_element(
                    ad_container, 'div[data-qa=POSTING_CARD_LOCATION]')
                if search_info.neighborhood.lower() in neighborhood.text.lower():
                    address = self._get_address(
                        neighborhood,
                        find_element(ad_container, '.sc-ge2uzh-0'))
                    price = self._get_price(find_element(
                        ad_container, 'div[data-qa=POSTING_CARD_PRICE]'))
                    features_list = ['' for i in range(5)]
                    features = find_elements(
                        ad_container,
                        'div[data-qa=POSTING_CARD_FEATURES] span span')
                    for e, feature in enumerate(features):
                        features_list[e] = self._get_from_feature(feature.text)
                    ads = find_elements(
                        self._driver,
                        '.sc-i1odl-2 .sc-i1odl-3 div:not([class]):first-child'
                    )
                    ad_url = self._get_ad_url(ads[i])
                    try:
                        phone_number = self._get_phone_number(find_element(
                            ad_container, 'button[data-qa=CARD_WHATSAPP'))
                        advertiser_name = self._get_advertiser_name(
                            find_element(ad_container,
                                         'button[data-qa=CARD_CONTACT_MODAL]'))
                    except Exception:
                        phone_number = 0
                        advertiser_name = ''
                    if ad_url not in list(dataframe['Link']):
                        real_estate = RealEstate(
                            negotiation_type=search_info.negotiation_type.lower(),
                            real_estate_type=search_info.real_estate_type.lower(),
                            city=f'{search_info.city} - {search_info.state}',
                            phone_number=phone_number,
                            price=price,
                            address=address,
                            area=features_list[0],
                            util_area=features_list[1],
                            bedrooms=features_list[2],
                            bathrooms=features_list[3],
                            car_spaces=features_list[4],
                            ad_url=ad_url,
                            advertiser_name=advertiser_name,
                        )
                        result.append(real_estate)
            try:
                url = find_element(
                    self._driver,
                    'a[data-qa=PAGING_NEXT]').get_attribute('href')
                self._driver.delete_all_cookies()
                self._driver.get(url)
                sleep(5)
            except TimeoutException:
                break
        return result

    def _get_price(self, price_element) -> float:
        return float(price_element.text[3:].replace('.', ''))

    def _get_phone_number(self, phone_number_element) -> str:
        self._driver.delete_all_cookies()
        self._driver.execute_script('arguments[0].click();',
                                    phone_number_element)
        sleep(5)
        current_window = self._driver.current_window_handle
        windows = self._driver.window_handles
        for w in windows:
            if w != current_window:
                self._driver.switch_to.window(w)
        regex = re.compile(r'.+phone=(\d+).+', re.DOTALL)
        url = find_element(self._driver, '#action-button').get_attribute(
            'href')
        phone_number = int(regex.findall(url)[0])
        self._driver.close()
        self._driver.switch_to.window(current_window)
        return phone_number

    def _get_address(self, neighborhood_element, address_element) -> str:
        return f'{address_element.text} - {neighborhood_element.text}'

    def _get_from_feature(self, feature: str) -> int:
        regex = re.compile(r'(\d+) .+', re.DOTALL)
        return int(regex.findall(feature)[0])

    def _get_ad_url(self, ad_element) -> str:
        self._driver.delete_all_cookies()
        self._driver.execute_script('arguments[0].click();', ad_element)
        current_window = self._driver.current_window_handle
        windows = self._driver.window_handles
        for w in windows:
            if w != current_window:
                self._driver.switch_to.window(w)
        url = self._driver.current_url
        self._driver.close()
        self._driver.switch_to.window(current_window)
        return url

    def _get_advertiser_name(self, advertiser_name_button) -> str:
        try:
            text = find_element(self._driver, 'h3.sc-ab7c1w-0').text
        except TimeoutException:
            return ''
        regex = re.compile(r'.+ WhatsApp para (.+) sobre o imóvel .+',
                           re.DOTALL)
        return regex.findall(text)[0]
