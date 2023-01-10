from typing import NamedTuple, List
from datetime import date
from forest_sangha_moons.MahanikayaCalendar import Season
from adjustments import get_seasons
from quick_icalendar_import import import_calendar

class Holiday(NamedTuple):
    holiday_name : str
    season_name : str
    uposatha : int
    holiday_date : str

def holidays_in(season : Season) -> List[Holiday]:
    holidays = []
    events = [event for event in season.events if event.special_day]
    for event in events:
        holiday = Holiday(
            holiday_name=event.special_day,
            season_name=season.season_name,
            uposatha=event.uposatha_of_season,
            holiday_date=event.date.isoformat()
        )
        holidays.append(holiday)
    return holidays

def all_holidays(seasons : List[Season]) -> List[Holiday]:
    holidays = []
    for season in seasons:
        holidays += holidays_in(season)
    return holidays

def display(holiday : Holiday):
    print(f"{holiday.holiday_date} {holiday.holiday_name} {holiday.season_name} {holiday.uposatha}")

def main():
    calendar = import_calendar(ical_file="../mahanikaya.ical")
    seasons = get_seasons(calendar)
    vesak_days = [holiday for holiday in all_holidays(seasons) if holiday.holiday_name == "Visākha Pūjā"]
    for holiday in vesak_days:
        display(holiday)

if __name__ == "__main__":
    main()