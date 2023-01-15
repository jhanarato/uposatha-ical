from datetime import date
from itertools import pairwise

from explore.calendar_extensions import get_seasons, add_date_before
from quick_icalendar_import import import_calendar

long_seq = [15, 15, 14, 15, 15, 15, 14, 15, 15, 15]
short_seq = [15, 15, 14, 15, 15, 15, 14, 15]


def season_is_long(season):
    return season.uposatha_count == 10

def days_between(first, last):
    delta = last - first
    return delta.days

def durations_sequence(season):
    dates = [season.date_before ] + [uposatha.date for uposatha in season.uposathas]
    return [days_between(start, end) for start, end in pairwise(dates)]

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