from calendar_extensions import add_date_before
from half_moons import *

# TODO: All [normal, extra month, extra day] seasons have the same sequence.

def test_normal_half_moons(seasons_including_date_before, normal_years):
    for season in seasons_including_date_before:
        if season.end_year in normal_years:
            assert days_between_half_moons(season) == [8, 15, 15, 14, 15, 15, 15, 14]