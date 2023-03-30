import pytest
import pandas as pd

from real_estate_scraping.use_cases import generate_spreadsheet
from real_estate_scraping.domain import RealEstate
from real_estate_scraping import exceptions


def test_generate_spreadsheet(real_estate) -> None:
    generate_spreadsheet([real_estate], 'tests/result.xlsx')
    df = pd.read_excel('tests/result.xlsx')
    assert pd.read_excel('tests/expected.xlsx').equals(df)


def test_generate_spreadsheet_with_invalid_extension(real_estate) -> None:
    with pytest.raises(exceptions.GenerateSpreadSheetError):
        generate_spreadsheet([real_estate], 'tests/result.pdf')
