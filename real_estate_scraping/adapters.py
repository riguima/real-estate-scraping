import re
from selenium.webdriver import Firefox
from selenium.common.exceptions import TimeoutException
import zapimoveis_scraper as zap
from slugify import slugify

from real_estate_scraping.domain import IBrowser, RealEstate
from real_estate_scraping.validators import valid_real_estate
from real_estate_scraping.use_cases import create_driver
from real_estate_scraping.helpers import find_element


class ZapImoveisBrowser(IBrowser):

    def __init__(self, driver: Firefox = None) -> None:
        self._driver = create_driver() if driver is None else driver

    def __del__(self) -> None:
        self._driver.close()

    def create_real_estates(self, city: str, state: str, negotiation_type: str,
                            real_estate_type: str) -> list[RealEstate]:
        result = []
        real_estates = zap.search(
            localization=f'{state.lower()}+{slugify(city)}', num_pages=1,
            acao=negotiation_type.lower(), tipo=real_estate_type.lower(),
        )[:2]
        for rs in real_estates:
            ad_url = f'https://www.zapimoveis.com.br{rs.link}'
            phone_number, advertiser_name = self._get_contact_info(ad_url)
            real_estate = RealEstate(
                negotiation_type=negotiation_type.lower(),
                real_estate_type=real_estate_type.lower(),
                city=f'{city} - {state}',
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
