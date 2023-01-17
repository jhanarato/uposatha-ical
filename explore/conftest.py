import datetime
import icalendar
import pytest

from explore.calendar_extensions import get_seasons, add_date_before
from forest_sangha_moons.MahanikayaCalendar import MahanikayaCalendar


@pytest.fixture(scope="module")
def icalendar_file():
    with open("../mahanikaya.ical", "r") as f:
        content = f.read()

    return content


@pytest.fixture(scope="module")
def parsed_ical(icalendar_file):
    return icalendar.Calendar.from_ical(icalendar_file)


@pytest.fixture
def imported_calendar(parsed_ical):
    calendar = MahanikayaCalendar()
    calendar.import_ical(parsed_ical)
    return calendar


@pytest.fixture
def seasons_list(imported_calendar):
    return get_seasons(imported_calendar)

@pytest.fixture
def seasons_including_date_before(seasons_list):
    add_date_before(seasons_list, datetime.date(2010, 2, 28))
    return seasons_list

@pytest.fixture
def extra_month_years():
    return [2010, 2012, 2015, 2018, 2021, 2023, 2026, 2029]

@pytest.fixture
def extra_day_years():
    return [2016, 2020, 2025, 2030]

@pytest.fixture
def normal_years(extra_month_years, extra_day_years):
    abnormal_years = extra_month_years + extra_day_years
    return [year for year in range(2010, 2031) if year not in abnormal_years]

@pytest.fixture
def cold_seasons(seasons_including_date_before):
    return [season for season in seasons_including_date_before if season.season_name == "Hemanta"]

@pytest.fixture
def rainy_seasons(seasons_including_date_before):
    return [season for season in seasons_including_date_before if season.season_name == "Vassāna"]

@pytest.fixture
def hot_seasons(seasons_including_date_before):
    return [season for season in seasons_including_date_before if season.season_name == "Gimha"]

@pytest.fixture
def extra_month_seasons(hot_seasons, extra_month_years):
    return [season for season in hot_seasons if season.end_year in extra_month_years]

@pytest.fixture
def extra_day_seasons(hot_seasons, extra_day_years):
    return [season for season in hot_seasons if season.end_year in extra_day_years]

