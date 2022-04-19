import datetime
import icalendar
from forest_sangha_moons import MahanikayaCalendar

with open("../mahanikaya.ical", "r") as f:
    content = f.read()

ical = icalendar.Calendar.from_ical(content)
calendar = MahanikayaCalendar()
calendar.import_ical(ical)

year = datetime.date.today().year

for season in calendar.seasons_in_year(year):
    print(season.end_date())