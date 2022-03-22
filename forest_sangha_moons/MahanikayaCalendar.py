import re
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
        if not self.events:
            self.events.append(Event(details))
        elif self.events[-1].date != details["date"]:
            self.events[-1].process()
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
        self.uposatha_days = 0

        self.phase_names = ["Full", "Waning", "New", "Waxing"]
        self.special_days = ["Āsāḷha Pūjā", "Māgha Pūjā", "Pavāraṇā Day", "Visākha Pūjā"]
        self.vassa_days = ["First day of Vassa", "Last day of Vassa"]
        self.extended_summary = None

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

    def _set_extended_summary(self):
        for summary in self.summaries:
            if "Full" in summary or "New" in summary:
                self.extended_summary = ExtendedSummary(summary)

    def process(self):
        self._set_moon_phase()
        self._set_special_days()
        self._set_vassa_days()
        self._set_extended_summary()

        if self.extended_summary:
            self.week_of_season = self.extended_summary.week_of_season()
            self.uposatha_days = self.extended_summary.uposatha_days()

    def __str__(self):
        """
        Pretty print the event.

        :return: A string representation of the Event.
        """
        outstr = "{}: {}".format(self.date.isoformat(), self.moon_name)
        if self.special_day:
            outstr += " : {}".format(self.special_day)
        if self.vassa_day:
            outstr += " : {}".format(self.vassa_day)
        if self.extended_summary:
            outstr += " : Week {}".format(self.week_of_season)
            outstr += " : Uposatha Days {}".format(self.uposatha_days)
        return outstr


class Season:
    def __init__(self, extended_summary):
        self.season_name = extended_summary.season_name()
        self.number_of_weeks = extended_summary.weeks_in_season()
        self.events = []

class ExtendedSummary():
    """
    Parser for summary text where there is extra information.

    Only the full and new moon summaries have extra information. This
    class provides methods for obtaining this information.

    Summary examples:
        "Full Moon - 15 day Hemanta 6/8"
        "New Moon - 14 day Gimha 3/10"
    """

    def __init__(self, summary):
        self.summary = summary

    def uposatha_days(self):
        if "15 day" in self.summary:
            return 15
        else:
            return 14
        # TODO: Throw an exception if neither found.

    def season_name(self):
        seasons = ["Hemanta", "Gimha", "Vassāna"]
        for season in seasons:
            if season in self.summary:
                return season
            # TODO: Throw an exception if the season is not found.

    def week_of_season(self):
        numbers = re.findall("[0-9]+", self.summary)
        return int(numbers[1])
        # TODO: Throw exception if not 3 numbers.

    def weeks_in_season(self):
        numbers = re.findall("[0-9]+", self.summary)
        return int(numbers[2])
        # TODO: Throw exception if not 3 numbers.


if __name__ == '__main__':
    content = ""
    with open("mahanikaya.ical", "r") as f:
        content = f.read()

    ical = icalendar.Calendar.from_ical(content)
    calendar = MahanikayaCalendar()
    calendar.import_ical(ical)

    print("Number of events: {}".format(len(calendar.events)))

    # Print a full lunar cycle
    for event in calendar.events[0:12]:
        print(event)

    # Print the pavarana
    pavaranas = [event for event in calendar.events if event.special_day == "Pavāraṇā Day"]

    for pavarana in pavaranas:
        print(pavarana)
