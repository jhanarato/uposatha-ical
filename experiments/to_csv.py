from forest_sangha_moons.MahanikayaCalendar import MahanikayaCalendar

from icalendar import Calendar
import csv

content = ""

with open("../mahanikaya.ical", "r") as f:
    content = f.read()

cal = Calendar.from_ical(content)
m_cal = MahanikayaCalendar(cal)
event_data = m_cal.all_events()

with open("events.csv", "w", newline="") as csvfile:
    cal_writer = csv.writer(csvfile)
    for event in event_data:
        cal_writer.writerow(event)

