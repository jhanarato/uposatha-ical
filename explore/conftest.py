import icalendar
import pytest

from explore.adjustments import get_seasons
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
