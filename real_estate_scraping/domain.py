from dataclasses import dataclass
from datetime import date


@dataclass
class RealEstate:
    negotiation_type: str
    type: str
    city: str
    phone_number: int
    price: float
    address: str
    area: int
    bedrooms: int
    bathrooms: int
    car_spaces: int
    publication_date: date
    ad_url: str
