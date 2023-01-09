from datetime import date, timedelta
import pytest

from quick_icalendar_import import import_calendar

cal = import_calendar(ical_file="../mahanikaya.ical")

def start_date(calendar):
    return calendar.seasons[0].events[-1].date

def get_seasons(calendar):
    return calendar.seasons[1:-1]

def uposathas_in_season(season):
    return [event for event in season.events if event.moon_name in ["Full", "New"]]

def season_is_long(season):
    return season.uposatha_count == 10

def print_long():
    for season in get_seasons(cal):
         if season_is_long(season):
            print(season)

def days_between(first, last):
    delta = last - first
    return delta.days

def uposatha_durations(date_before, season):
    uposathas = uposathas_in_season(season)
    durations = []
    uposatha_date = uposathas[0].date
    durations.append(days_between(date_before, uposatha_date))

    for uposatha in uposathas[1:]:
        duration = days_between(uposatha_date, uposatha.date)
        durations.append(duration)
        uposatha_date = uposatha.date

    return durations

@pytest.fixture
def imported_calendar():
    return import_calendar(ical_file="../mahanikaya.ical")

def test_uposatha_durations(imported_calendar):
    date_before = start_date(imported_calendar)
    season = get_seasons(imported_calendar)[0]

    durations = uposatha_durations(date_before, season)

    expected = [15, 15,
                14, 15,
                15, 15,
                14, 15,
                15, 15]

    assert durations == expected