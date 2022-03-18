from forest_sangha_moons.MahanikayaCalendar import MahanikayaCalendar

from icalendar import Calendar

content = ""

with open("../mahanikaya.ical", "r") as f:
    content = f.read()

cal = Calendar.from_ical(content)

m_cal = MahanikayaCalendar(cal)

print("Number of events: {}".format(m_cal.number_of_events()))
