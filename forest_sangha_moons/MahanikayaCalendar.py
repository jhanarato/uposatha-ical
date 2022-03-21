import icalendar

def extract_details(icalendar):
    """
    Generate event details from an icalendar

    This specifically works with the current version of the Maha Nikaya icalendar
    file used to generate the Forest Sangha calendars. The file is available here:

    http://splendidmoons.github.io/ical/mahanikaya.ical

    :param icalendar: The contents of the icalendar as a string.
    :returns: A dictionary with 'keys' date & 'summary'
    """
    for component in icalendar.walk():
        if component.name == "VEVENT":
            dtstart = component.get("DTSTART")
            summary = component.get("SUMMARY")
            if dtstart != None and summary != None:
                yield {"date": dtstart.dt, "summary": summary}


class MahanikayaCalendar:
    """
    Manages the importing of the Maha Nikaya lunar calendar
    """
    def __init__(self):
        self.events = []
        self.seasons = []

    def import_ical(self, icalendar):
        """
        Read in the details from the Splendid Moons icalendar file.

        Assumptions are made about the file contents. Future changes to
        its format could potentially break this method. After importing
        the events and seasons lists will be populated.

        :param icalendar: an icalendar.Calendar object
        """
        for details in extract_details(icalendar):
            self._process_details(details)

    def _process_details(self, details):
        """
        This is called whenever we get a pair of dates & summaries.

        More than one detail might be associated with a given date. Events
        are added or updated and kept in the event list.

        :param details: A dictionary with 'keys' date & 'summary'.
        """
        # For the first event or when the date changes, create a new event.
        if not self.events or self.events[-1].date != details["date"]:
            self.events.append(Event(details))
        else:
            self.events[-1].update(details)

class Event:
    """
    Represents an event in the Maha Nikaya calendar.

    Each event falls on a moon day, i.e. waning, new, waxing or full. The one
    exception to this is the first day of the rains retreat. Some events will
    also be a "special" day, such as Māgha Pūjā. icalendar data is passed to
    the Event object and it is responsible for parsing that data and setting
    its own state.
    """

    def __init__(self, details):
        """
        Initialises the event

        :param details: The first details, a dictionary with 'keys' date & 'summary'
        """
        self.date = details["date"]
        self.summaries = [details["summary"]]

        self.moon_name = ""
        self.special_day = ""
        self.vassa_day = ""

        self.season = None
        self.week_of_season = 0

        self.phase_names = ["Full", "Waning", "New", "Waxing"]
        self.special_days = ["Āsāḷha Pūjā", "Māgha Pūjā", "Pavāraṇā Day", "Visākha Pūjā"]
        self.vassa_days = ["First day of Vassa", "Last day of Vassa"]

    def update(self, details):
        """
        Update an initialised event with extra details.

        :param details: extra information, a dictionary with 'keys' date & 'summary'
        :return:
        """
        self.summaries.append(details["summary"])

    def _set_moon_phase(self):
        """ Set the moon phase for this event using the summary data. """
        for summary in self.summaries:
            first_word = summary.split()[0]
            if first_word in self.phase_names:
                self.moon_name = first_word
                return
            else:
                # Only "First day of Vassa" does not fall on a moon day.
                self.moon_name = "None"

    def _set_special_days(self):
        """ Set the special day, if there is one """
        for summary in self.summaries:
            if summary in self.special_days:
                self.special_day = summary

    def _set_vassa_days(self):
        """ Set the first & last days of the vassa (i.e. rains retreat) """
        for summary in self.summaries:
            if summary in self.vassa_days:
                self.vassa_day = summary

    def process(self):
        self._set_moon_phase()
        self._set_special_days()
        self._set_vassa_days()

    def __str__(self):
        """
        Pretty print the event.

        :return: A string representation of the Event.
        """
        outstr = self.date.isoformat()
        for summary in self.summaries:
            outstr = outstr + "\n  {}".format(summary)
        return outstr


class Season:
    def __init__(self):
        self.season_name = ""
        self.number_of_weeks = 0
        self.events = []


if __name__ == '__main__':
    content = ""
    with open("mahanikaya.ical", "r") as f:
        content = f.read()

    ical = icalendar.Calendar.from_ical(content)
    calendar = MahanikayaCalendar()
    calendar.import_ical(ical)

    print("Number of events: {}".format(len(calendar.events)))

    # Print a full lunar cycle
    for event in calendar.events[0:4]:
        print(event)


