from forest_sangha_moons.MahanikayaCalendar import MahanikayaCalendar

from icalendar import Calendar

# Bring in all the events to experiment with the data structure
content = ""
with open("../mahanikaya.ical", "r") as f:
    content = f.read()

cal = Calendar.from_ical(content)
m_cal = MahanikayaCalendar(cal)
events = m_cal.all_events()

# How to merge events on the same day?
for event in events:
    same_as = [same for same in events if event[1] == same[1]]
    if len(same_as) > 1:
        print(len(same_as))

# How to interpolate week numbers for waxing / waning moon days?