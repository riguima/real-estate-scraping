import pytest
import pandas as pd

from real_estate_scraping.use_cases import to_excel
from real_estate_scraping.domain import RealEstate
from real_estate_scraping import exceptions


def test_to_excel(real_estate) -> None:
    to_excel([real_estate], 'tests/result.xlsx')
    df = pd.read_excel('tests/result.xlsx')
    assert pd.read_excel('tests/expected.xlsx').equals(df)


def test_to_excel_with_invalid_extension(real_estate) -> None:
    with pytest.raises(exceptions.ToExcelError):
        to_excel([real_estate], 'tests/result.pdf')
