import datetime
import icalendar
from forest_sangha_moons import MahanikayaCalendar

with open("../mahanikaya.ical", "r") as f:
    content = f.read()

ical = icalendar.Calendar.from_ical(content)
calendar = MahanikayaCalendar()
calendar.import_ical(ical)

year = datetime.date.today().year

for special_day in calendar.special_days_in_year(year):
    date_str = special_day.date.strftime("%d-%m-%y")
    print("{} {}".format(date_str, special_day.special_day))