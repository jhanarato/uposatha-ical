from datetime import date, timedelta
from itertools import pairwise

import pytest

from quick_icalendar_import import import_calendar

long_seq = [15, 15, 14, 15, 15, 15, 14, 15, 15, 15]
short_seq = [15, 15, 14, 15, 15, 15, 14, 15]

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

def durations_sequence(season):
    dates = [season.date_before ] + [uposatha.date for uposatha in season.uposathas]
    durations = []
    for pair_of_dates in pairwise(dates):
        durations.append(
            days_between(pair_of_dates[0], pair_of_dates[1])
        )

    return durations

def adjusted_seasons(seasons_list):
    add_date_before(seasons_list, date(2010, 2, 28))
    adjusted = []

    for season in seasons_list:
        if season.uposatha_count == 8:
            if durations_sequence(season) != short_seq:
                adjusted.append(season)
        if season.uposatha_count == 10:
            if durations_sequence(season) != long_seq:
                adjusted.append(season)

    return adjusted

def main():
    calendar = import_calendar(ical_file="../mahanikaya.ical")
    seasons = get_seasons(calendar)
    add_date_before(seasons, date(2010, 2, 28))
    adjusted = adjusted_seasons(seasons)
    for season in adjusted:
        name = season.season_name
        year = season.events[0].date.year
        sequence = durations_sequence(season)
        print(f"{ name } season { year }: { sequence }")


if __name__ == "__main__":
    main()