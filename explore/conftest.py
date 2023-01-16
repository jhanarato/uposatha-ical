import datetime
import icalendar
import pytest

from explore.calendar_extensions import get_seasons
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
def extra_month_years():
    return [2010, 2012, 2015, 2018, 2021, 2023, 2026, 2029]

@pytest.fixture
def extra_day_years():
    return [2016, 2020, 2025, 2030]