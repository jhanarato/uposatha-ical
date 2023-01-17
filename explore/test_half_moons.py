import pytest
from calendar_extensions import add_date_before
from half_moons import *

def test_all_seasons_in_normal_year(seasons_including_date_before, normal_years):
    for season in seasons_including_date_before:
        if season.end_year in normal_years:
            assert days_between_half_moons(season) == [8, 15, 15, 14, 15, 15, 15, 14]

def test_extra_month_in_hot_season(seasons_including_date_before, extra_month_years):
    seasons = [ season for season in seasons_including_date_before if season.season_name == "Gimha"]
    seasons = [season for season in seasons if season.end_year in extra_month_years]

    for season in seasons:
        assert days_between_half_moons(season) == [8, 15, 15, 14, 15, 15, 15, 14, 15, 15]

def test_cold_seasons(cold_seasons):
    for season in cold_seasons:
        assert days_between_half_moons(season) == [8, 15, 15, 14, 15, 15, 15, 14]

def test_rainy_seasons(rainy_seasons):
    for season in rainy_seasons:
        assert days_between_half_moons(season) == [8, 15, 15, 14, 15, 15, 15, 14]

def test_extra_month_seasons(extra_month_seasons):
    for season in extra_month_seasons:
        assert days_between_half_moons(season) == [8, 15, 15, 14, 15, 15, 15, 14, 15, 15]

def test_extra_day_seasons(extra_day_seasons):
    for season in extra_day_seasons:
        assert days_between_half_moons(season) == [8, 15, 15, 14, 15, 15, 15, 15]