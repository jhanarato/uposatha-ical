from datetime import date

import pytest

from forest_sangha_moons.MahanikayaCalendar import MahanikayaCalendar, SeasonMaker

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

def initialise_calendar(details):
    """ This is adapted from import_ical() """
    cal = MahanikayaCalendar()
    for detail in details:
        cal._process_details(detail)
    cal._complete_event()
    season_maker = SeasonMaker(cal.events)
    cal.seasons = season_maker.get_seasons()
    return cal

@pytest.fixture
def first_month_of_cold_season_details():
    return [
        {"date": date(2010, 11, 29), "summary": "Waning Moon"},
        {"date": date(2010, 12, 6), "summary": "New Moon - 15 day Hemanta 1/8"},
        {"date": date(2010, 12, 14), "summary": "Waxing Moon"},
        {"date": date(2010, 12, 21), "summary": "Full Moon - 15 day Hemanta 2/8"}
    ]

@pytest.fixture
def one_month_of_events(first_month_of_cold_season_details):
    return initialise_calendar(first_month_of_cold_season_details)
