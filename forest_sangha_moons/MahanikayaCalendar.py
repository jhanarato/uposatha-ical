from icalendar import Calendar
from icalendar.cal import Component


def extract_details(icalendar):
    """
    Generate event details from an icalendar

    This specifically works with the current version of the Maha Nikaya icalendar
    file used to generate the Forest Sangha calendars. The file is available here:

    http://splendidmoons.github.io/ical/mahanikaya.ical

    :param icalendar: The contents of the icalendar as a string.
    :returns: A dictionary with two values: date and summary
    """
    for component in icalendar.walk():
        if component.name == "VEVENT":
            dtstart = component.get("DTSTART")
            summary = component.get("SUMMARY")
            if dtstart != None and summary != None:
                yield {"date": dtstart.dt, "summary": summary}


class MahanikayaCalendar:
    def __init__(self):
        self.events = []

    def import_ical(self, icalendar):
        for details in extract_details(icalendar):
            self._process_details(details)

    def _process_details(self, details):
        # For the first event or when the date changes, create a new event.
        if not self.events or self.events[-1].date != details["date"]:
            self.events.append(Event(details))
        else:
            self.events[-1].update(details)


class Event:
    def __init__(self, details):
        self.date = details["date"]
        self.summaries = [details["summary"]]

        self.moon_phase = ""
        self.special_day = ""

        self.season = ""
        self.week_of_season = -1
        self.weeks_in_season = -1

    def update(self, details):
        self.summaries.append(details["summary"])

    def __str__(self):
        outstr = self.date.isoformat()
        for summary in self.summaries:
            outstr = outstr + "\n  {}".format(summary)
        return outstr

if __name__ == '__main__':
    content = ""
    with open("../mahanikaya.ical", "r") as f:
        content = f.read()

    ical = Calendar.from_ical(content)
    calendar = MahanikayaCalendar()
    calendar.import_ical(ical)

    print("Number of events: {}".format(len(calendar.events)))

    # Print a full lunar cycle
    for event in calendar.events[0:4]:
        print(event)


