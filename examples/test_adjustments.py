from datetime import date, timedelta
import pytest
import icalendar
from forest_sangha_moons.MahanikayaCalendar import MahanikayaCalendar

from adjustments import *

@pytest.fixture(scope="module")
def ical_content():
    with open("../mahanikaya.ical", "r") as f:
        content = f.read()

    return content

@pytest.fixture(scope="module")
def parsed_ical(ical_content):
    return icalendar.Calendar.from_ical(ical_content)

@pytest.fixture
def imported_calendar(parsed_ical):
    calendar = MahanikayaCalendar()
    calendar.import_ical(parsed_ical)
    return calendar

@pytest.fixture
def seasons_list(imported_calendar):
    return get_seasons(imported_calendar)

@pytest.mark.parametrize(
    "season_index,date_before",
    [
        (0, date(2010, 2, 28)),
        (1, date(2010, 7, 26))
    ]
)
def test_date_before_season(seasons_list, season_index, date_before):
    season = seasons_list[season_index]
    uposathas = season.uposathas
    assert uposathas[0].date - timedelta(15) == date_before

@pytest.mark.parametrize(
    "season_index,first_date",
    [
        (0, date(2010, 3, 15)),
        (1, date(2010, 8, 10))
    ]
)
def test_first_date_second_season(seasons_list, season_index, first_date):
    second_season = seasons_list[season_index]
    first_uposatha = second_season.uposathas[0]
    assert first_uposatha.date == first_date

@pytest.mark.parametrize(
    "season_index,date_before",
    [
        (0, date(2010, 2, 28)),
        (1, date(2010, 7, 26)),
        (2, date(2010, 11, 21))
    ]
)
def test_add_date_before(seasons_list, season_index, date_before):
    add_date_before(seasons_list, date(2010, 2, 28))
    date_before = seasons_list[season_index].date_before
    assert date_before == date_before

@pytest.mark.parametrize(
    "season_index,expected_sequence",
    [
        (0, long_seq),
        (1, short_seq)
    ]
)
def test_season_to_duration_sequence(seasons_list, season_index, expected_sequence):
    add_date_before(seasons_list, date(2010, 2, 28))
    first_season = seasons_list[season_index]
    sequence = durations_sequence(first_season)
    assert sequence == expected_sequence