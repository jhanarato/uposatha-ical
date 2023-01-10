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
    assert 0