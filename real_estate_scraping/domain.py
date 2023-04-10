from dataclasses import dataclass
from datetime import date, datetime
from abc import ABC, abstractmethod
import pandas as pd


@dataclass
class RealEstate:
    negotiation_type: str
    real_estate_type: str
    city: str
    phone_number: int
    price: float
    address: str
    area: int
    bedrooms: int
    bathrooms: int
    car_spaces: int
    ad_url: str
    util_area: int = ''
    publication_date: date = datetime.now().date()
    advertiser_name: str = ''


@dataclass
class SearchInfo:
    city: str
    state: str
    neighborhood: str
    negotiation_type: str
    real_estate_type: str
    num_pages: int


class IBrowser(ABC):

    @abstractmethod
    def create_real_estates(self, search_info: SearchInfo,
                            dataframe: pd.DataFrame) -> RealEstate:
        raise NotImplementedError()
