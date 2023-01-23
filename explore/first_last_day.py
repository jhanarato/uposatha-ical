from explore.quick_icalendar_import import import_calendar
import os
from datetime import date, timedelta

os.chdir("/home/jr/Code/uposatha-ical")
cal = import_calendar()
seasons_of_interest = [season for season in cal.seasons if season.events[0].date.year in [2011, 2012]]

for season in seasons_of_interest:
    first_uposatha = season.events[1]
    last_uposatha = season.events[-1]
    first_day = first_uposatha.date - timedelta(14)
    last_day = last_uposatha.date
    print(f"{season.english_name():<6} {first_day.isoformat()} {last_day.isoformat()}")