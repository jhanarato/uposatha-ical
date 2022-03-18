from icalendar import Calendar
from forest_sangha_moons.MahanikayaCalendar import MahanikayaCalendar
content = ""
with open("mahanikaya.ical", "r") as f:
    content = f.read()

ical = Calendar.from_ical(content)
calendar = MahanikayaCalendar()
calendar.import_ical(ical)

print("Number of events: {}".format(len(calendar.events)))

# Print a full lunar cycle

two_summaries = [event for event in calendar.events if len(event.summaries) == 2]
three_summaries = [event for event in calendar.events if len(event.summaries) == 3]

for event in three_summaries:
    print(event)