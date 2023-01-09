from datetime import date, timedelta
import pytest

from quick_icalendar_import import import_calendar

long_seq = [15, 15, 14, 15, 15, 15, 14, 15, 15, 15]
short_seq = [15, 15, 14, 15, 15, 15, 14, 15]

cal = import_calendar(ical_file="../mahanikaya.ical")

def start_date(calendar):
    return calendar.seasons[0].events[-1].date

def get_seasons(calendar):
    return calendar.seasons[1:-1]

def season_is_long(season):
    return season.uposatha_count == 10

def days_between(first, last):
    delta = last - first
    return delta.days

def add_date_before(seasons, date_before_first_season):
    season_iter = iter(seasons)
    season = next(season_iter)
    season.date_before = date_before_first_season

    for next_season in season_iter:
        date_before = season.uposathas[-1].date
        next_season.date_before = date_before
        season = next_season

def duration_sequence(season):
    dates = [ season.date_before ]
    for uposatha in season.uposathas:
        dates.append(uposatha.date)

    durations = []

    for i, _ in enumerate(dates):
        if i > 0:
            durations.append(
                days_between(dates[i - 1], dates[i])
            )

    return durations