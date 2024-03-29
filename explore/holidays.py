import datetime
from typing import NamedTuple, List
from datetime import date
from forest_sangha_moons.MahanikayaCalendar import Season
from explore.calendar_extensions import get_seasons
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

def holiday_dates(holidays : List[Holiday]) -> List[date]:
    return [holiday.holiday_date for holiday in holidays]

def season_is_long(season : Season) -> bool:
    return season.uposatha_count == 10

def cold_season_magha_puja_uposatha(cold_season : Season) -> int:
    for event in cold_season.events:
        if event.special_day == MAGHA_PUJA:
            return event.uposatha_of_season
    raise RuntimeError("Not a cold day with a magha puja")

def display(holiday : Holiday):
    print(f"{holiday.holiday_date.isoformat()} {holiday.holiday_name} {holiday.season_name} {holiday.uposatha}")

def show_selected_holiday_info():
    calendar = import_calendar(ical_file="../mahanikaya.ical")
    seasons = get_seasons(calendar)
    for holiday_name in [VESAK_DAY, MAGHA_PUJA]:
        holidays = filter_by_name(all_holidays(seasons), holiday_name)
        print(holiday_name)
        for holiday in holidays:
            display(holiday)

def show_dates(holiday_name):
    calendar = import_calendar(ical_file="../mahanikaya.ical")
    seasons = get_seasons(calendar)
    holidays = filter_by_name(all_holidays(seasons), holiday_name)
    dates = holiday_dates(holidays)
    print(f"{holiday_name} dates:")
    for holiday_date in dates:
        print(holiday_date)

if __name__ == "__main__":
    show_dates(VESAK_DAY)
    show_dates(MAGHA_PUJA)
    show_dates(PAVARANA_DAY)
    show_dates(ASALHA_PUJA)