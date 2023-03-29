from domain import RealEstate


def valid_real_estate(real_estate: RealEstate) -> None:
    validation_functions = [
        valid_negotiation_type, is_valid_city,
        valid_phone_number, is_valid_address, is_valid_publication_date,
        valid_ad_url]
    for f in validation_functions:
        f(real_estate)
