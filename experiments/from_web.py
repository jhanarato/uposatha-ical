from forest_sangha_moons.MahanikayaCalendar import MahanikayaCalendar

import requests
from icalendar import Calendar

url = "http://splendidmoons.github.io/ical/mahanikaya.ical"

response = requests.get(url)
content = response.content

cal = Calendar.from_ical(content)
m_cal = MahanikayaCalendar(cal)

print("Number of events: {}".format(m_cal.number_of_events()))
