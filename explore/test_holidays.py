from datetime import date

import pytest

from holidays import *

@pytest.fixture
def holidays(seasons_list):
    return all_holidays(seasons_list)

@pytest.fixture
def asalha_pujas(holidays):
    return filter_by_name(holidays, ASALHA_PUJA)

@pytest.fixture
def pavarana_days(holidays):
    return filter_by_name(holidays, PAVARANA_DAY)

@pytest.fixture
def vesak_days(holidays):
    return filter_by_name(holidays, VESAK_DAY)

@pytest.fixture
def magha_pujas(holidays):
    return filter_by_name(holidays, MAGHA_PUJA)

def test_asalhas(asalha_pujas):
    for holiday in asalha_pujas:
        assert holiday.uposatha in [8, 10]
        assert holiday.season_name == HOT_SEASON

def test_pavaranas(pavarana_days):
    for holiday in pavarana_days:
        assert holiday.uposatha == 6
        assert holiday.season_name == RAINY_SEASON

def test_vesak_in_may_or_june(vesak_days):
    for holiday in vesak_days:
        assert holiday.holiday_date.month in [5, 6]

def test_magha_in_feb_or_mar(magha_pujas):
    for holiday in magha_pujas:
        assert holiday.holiday_date.month in [2, 3]
