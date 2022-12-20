import pytest

from forest_sangha_moons.MahanikayaCalendar import MahanikayaCalendar, SeasonMaker


@pytest.fixture
def x():
    return "x"


def details_to_seasons(details):
    cal = MahanikayaCalendar()
    for moon in details:
        cal._process_details(moon)
    cal._complete_event()
    maker = SeasonMaker(cal.events)
    return maker.get_seasons()


def details_to_events(details):
    cal = MahanikayaCalendar()
    for moon in details:
        cal._process_details(moon)
    cal._complete_event()
    return cal.events
