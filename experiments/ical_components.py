from icalendar import Calendar

content = ""

with open("../mahanikaya.ical", "r") as f:
    content = f.read()

ical = Calendar.from_ical(content)

for component in ical.walk():
    if component.name == "VCALENDAR":
        print("Calendar")

event_count = 0

for component in ical.walk():
    if component.name == "VEVENT":
        event_count = event_count + 1

print("{} events".format(event_count))
