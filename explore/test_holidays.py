from datetime import date

import pytest

from holidays import *

@pytest.fixture
def holidays(seasons_list):
    return all_holidays(seasons_list)

def test_asalha(holidays):
    asalha_holidays = filter_by_name(holidays, ASALHA_PUJA)

    for holiday in asalha_holidays:
        assert holiday.uposatha in [8, 10]
        assert holiday.season_name == HOT_SEASON

def test_pavarana(holidays):
    pavaranas = filter_by_name(holidays, PAVARANA_DAY)

    for holiday in pavaranas:
        assert holiday.uposatha == 6
        assert holiday.season_name == RAINY_SEASON

def test_vesak_always_in_may_or_june(holidays):
    vesak_days = filter_by_name(holidays, VESAK_DAY)

    for holiday in vesak_days:
        date_ = date.fromisoformat(holiday.holiday_date)
        assert date_.month in [5, 6]