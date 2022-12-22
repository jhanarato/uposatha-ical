from datetime import date

from forest_sangha_moons.MahanikayaCalendar import Season
from conftest import details_to_seasons

def test_end_date():
    details = [
        {"date": date(2010, 11, 29), "summary": "Waning Moon"},
        {"date": date(2010, 12, 6), "summary": "New Moon - 15 day Hemanta 1/8"},
        {"date": date(2010, 12, 14), "summary": "Waxing Moon"},
        {"date": date(2010, 12, 21), "summary": "Full Moon - 15 day Hemanta 2/8"}
    ]

    season = details_to_seasons(details)[0]
    assert season.end_date() == date(2010, 12, 21)

def test_english_name():
    season = Season()
    season.season_name = "Hemanta"
    assert season.english_name() == "Cold"

    season.season_name = "Gimha"
    assert season.english_name() == "Hot"

    season.season_name = "Vassāna"
    assert season.english_name() == "Rainy"