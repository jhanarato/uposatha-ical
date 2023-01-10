import datetime
from typing import NamedTuple, List
from datetime import date
from forest_sangha_moons.MahanikayaCalendar import Season
from adjustments import get_seasons
from quick_icalendar_import import import_calendar

VESAK_DAY = "Visākha Pūjā"
ASALHA_PUJA = "Āsāḷha Pūjā"
MAGHA_PUJA = "Māgha Pūjā"
PAVARANA_DAY = "Pavāraṇā Day"

COLD_SEASON = "Hemanta"
HOT_SEASON = "Gimha"
RAINY_SEASON = "Vassāna"

class Holiday(NamedTuple):
    holiday_name : str
    season_name : str
    uposatha : int
    holiday_date : date

def holidays_in(season : Season) -> List[Holiday]:
    holidays = []
    events = [event for event in season.events if event.special_day]
    for event in events:
        holiday = Holiday(
            holiday_name=event.special_day,
            season_name=season.season_name,
            uposatha=event.uposatha_of_season,
            holiday_date=event.date
        )
        holidays.append(holiday)
    return holidays

def all_holidays(seasons : List[Season]) -> List[Holiday]:
    holidays = []
    for season in seasons:
        holidays += holidays_in(season)
    return holidays

def filter_by_name(holidays : List[Holiday], name) -> List[Holiday]:
    return [holiday for holiday in holidays if holiday.holiday_name == name]

def display(holiday : Holiday):
    print(f"{holiday.holiday_date.isoformat()} {holiday.holiday_name} {holiday.season_name} {holiday.uposatha}")

def main():
    calendar = import_calendar(ical_file="../mahanikaya.ical")
    seasons = get_seasons(calendar)
    for holiday_name in [VESAK_DAY, MAGHA_PUJA]:
        holidays = filter_by_name(all_holidays(seasons), holiday_name)
        print(holiday_name)
        for holiday in holidays:
            display(holiday)

if __name__ == "__main__":
    main()