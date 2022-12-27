from datetime import date

from forest_sangha_moons.MahanikayaCalendar import Season
from conftest import details_to_seasons, first_month_of_cold_season

def test_end_date():
    details = first_month_of_cold_season()
    season = details_to_seasons(details)[0]
    assert season.end_date() == date(2010, 12, 21)

# TODO Parameterize
def test_english_name():
    season = Season()
    season.season_name = "Hemanta"
    assert season.english_name() == "Cold"

    season.season_name = "Gimha"
    assert season.english_name() == "Hot"

    season.season_name = "Vassāna"
    assert season.english_name() == "Rainy"