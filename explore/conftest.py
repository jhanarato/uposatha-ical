import icalendar
import pytest


@pytest.fixture(scope="module")
def icalendar_file():
    with open("../mahanikaya.ical", "r") as f:
        content = f.read()

    return content


@pytest.fixture(scope="module")
def parsed_ical(icalendar_file):
    return icalendar.Calendar.from_ical(icalendar_file)
