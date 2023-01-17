from half_moons import *

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