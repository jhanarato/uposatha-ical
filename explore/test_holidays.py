from holidays import *

def test_holidays(seasons_list):
    assert holidays_in(seasons_list[0])