import pytest

from forest_sangha_moons.MahanikayaCalendar import MahanikayaCalendar, SeasonMaker

# TODO Make this a fixture
def details_to_seasons(details):
    cal = MahanikayaCalendar()
    for moon in details:
        cal._process_details(moon)
    cal._complete_event()
    maker = SeasonMaker(cal.events)
    return maker.get_seasons()

# TODO Make this a fixture
def details_to_events(details):
    cal = MahanikayaCalendar()
    for moon in details:
        cal._process_details(moon)
    cal._complete_event()
    return cal.events

# TODO Make this a fixture
def initialise_calendar(details):
    """ This is adapted from import_ical() """
    cal = MahanikayaCalendar()
    for detail in details:
        cal._process_details(detail)
    cal._complete_event()
    season_maker = SeasonMaker(cal.events)
    cal.seasons = season_maker.get_seasons()
    return cal
