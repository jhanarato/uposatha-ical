from icalendar import Calendar
from icalendar.cal import Component


class MahanikayaCalendar:
    def __init__(self, icalendar):
        self._icalendar = icalendar
        self._events = []
        self.import_ical(ical)

    def extract_details(self):
        for component in self._icalendar.walk():
            if component.name == "VEVENT":
                dtstart = component.get("DTSTART")
                summary = component.get("SUMMARY")
                if dtstart != None and summary != None:
                    yield {"date": dtstart.dt, "summary": summary}

    def import_ical(self, ical):
        current_event = None
        for details in self.extract_details():
            if current_event is None:
                current_event = Event(details["date"])

            if current_event.date != details["date"]:
                current_event = Event(details["date"])

            current_event.add_summary(details["summary"])
            self._events.append(current_event)




    def number_of_events(self):
        return len(self._events)

    def all_events(self):
        return self._events


class Event:
    def __init__(self, date):
        self.date = date
        self.summaries = []

        self.moon_phase = ""
        self.special_day = ""

        self.season = ""
        self.week_of_season = -1
        self.weeks_in_season = -1

    def add_summary(self, summary):
        self.summaries.append(summary)

    def __str__(self):
        outstr = self.date.isoformat()
        for summary in self.summaries:
            outstr = outstr + "\n  {}".format(summary)
        return outstr

if __name__ == '__main__':
    content = ""
    with open("mahanikaya.ical", "r") as f:
        content = f.read()

    ical = Calendar.from_ical(content)
    calendar = MahanikayaCalendar(ical)

    print("Number of events: {}".format(calendar.number_of_events()))

    # Print a full lunar cycle
    for event in calendar.all_events()[0:4]:
        print(event)


