from typing import NamedTuple, List

from forest_sangha_moons.MahanikayaCalendar import Season
from adjustments import get_seasons
from quick_icalendar_import import import_calendar

class Holiday(NamedTuple):
    holiday_name : str
    season_name : str
    year : int

def holidays_in(season : Season) -> List[Holiday]:
    holidays = []
    events = [event for event in season.events if event.special_day]
    for event in events:
        holiday = Holiday(
            holiday_name=event.special_day,
            season_name=season.season_name,
            year=season.events[-1].date.year
        )
        holidays.append(holiday)
    return holidays

def all_holidays(seasons : List[Season]) -> List[Holiday]:
    holidays = []
    for season in seasons:
        holidays += holidays_in(season)
    return holidays


def display(holiday : Holiday):
    print(f"{holiday.year} {holiday.season_name} {holiday.holiday_name}")

def main():
    calendar = import_calendar(ical_file="../mahanikaya.ical")
    seasons = get_seasons(calendar)
    for holiday in all_holidays(seasons):
        display(holiday)

if __name__ == "__main__":
    main()