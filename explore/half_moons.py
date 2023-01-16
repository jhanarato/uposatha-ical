from datetime import date
from itertools import pairwise

from quick_icalendar_import import import_calendar
from calendar_extensions import add_date_before, get_seasons

def half_moon_dates(season):
    return [moon.date for moon in season.half_moons]

def days_between_half_moons(season):
    dates = [season.date_before ] + half_moon_dates(season)
    return [(second - first).days for first, second in pairwise(dates)]

def main():
    calendar = import_calendar(ical_file="../mahanikaya.ical")
    seasons = get_seasons(calendar)
    add_date_before(seasons, date(2010, 2, 28))
    sequence = days_between_half_moons(seasons[1])
    print(sequence)

    for season in seasons:
        year = season.end_year
        season_name = season.season_name
        sequence = days_between_half_moons(season)
        print(f"{year} {season_name :<8} { sequence }")

if __name__ == "__main__":
    main()