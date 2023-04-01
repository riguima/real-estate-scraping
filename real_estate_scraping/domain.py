from dataclasses import dataclass
from datetime import date, datetime
from abc import ABC, abstractmethod


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
    publication_date: date = datetime.now().date()
    advertiser_name: str = ''


class IBrowser(ABC):

    @abstractmethod
    def create_real_estates(self) -> RealEstate:
        raise NotImplementedError()
