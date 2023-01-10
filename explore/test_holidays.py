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

@pytest.fixture
def vesak_dates(vesak_days):
    return holiday_dates(vesak_days)

@pytest.fixture
def magha_dates(magha_pujas):
    return holiday_dates(magha_pujas)

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

def test_vesak_dates(vesak_dates):
    assert len(vesak_dates) == 21

def test_magha_dates(magha_dates):
    assert len(magha_dates) == 20

def test_vesak_is_fourth_in_normal_hot_season(seasons_list):
    hot_seasons = [season for season in seasons_list if season.season_name == HOT_SEASON]
    short_hot_seasons = [season for season in hot_seasons if season.uposatha_count == 8]

    for season in short_hot_seasons:
        for event in season.events:
            if event.special_day == VESAK_DAY:
                assert event.uposatha_of_season == 4

def test_vesak_is_sixth_in_long_hot_season(seasons_list):
    hot_seasons = [season for season in seasons_list if season.season_name == HOT_SEASON]
    long_hot_seasons = [season for season in hot_seasons if season.uposatha_count == 10]

    for season in long_hot_seasons:
        for event in season.events:
            if event.special_day == VESAK_DAY:
                assert event.uposatha_of_season == 6