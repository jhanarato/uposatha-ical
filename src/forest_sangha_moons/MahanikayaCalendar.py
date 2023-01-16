import re
import icalendar
import datetime

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

        # Set the current day and store it. Having this as
        # a class member makes testing easier.
        self.today = datetime.date.today()

        self.events = []
        self.seasons = []

        self._incomplete_event = None
        self._incomplete_season = None

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

        # Complete the last event.
        self._complete_event()

        season_maker = SeasonMaker(self.events)
        self.seasons = season_maker.get_seasons()

    def _process_details(self, details):
        """
        This is called whenever we get a pair of dates & summaries.

        More than one detail might be associated with a given date. Events
        are added or updated and kept in the event list.

        :param details: A dictionary with 'keys' date & 'summary'.
        """
        self._update_events(details)

    def _update_events(self, details):
        if not self._incomplete_event:
            self._incomplete_event = Event(details)
        elif self._new_date(details):
            self._complete_event()
            self._incomplete_event = Event(details)
        else:
            self._incomplete_event.add_details(details)

    def _new_date(self, details):
        return self._incomplete_event.date != details["date"]

    def _complete_event(self):
        self._incomplete_event.complete()
        complete_event = self._incomplete_event
        self.events.append(complete_event)

    def next_event(self):
        for an_event in self.events:
            if an_event.date > self.today:
                return an_event
        # TODO: Raise exception.
        return None

    def next_uposatha(self):
        for uposatha in self.get_uposathas():
            if uposatha.date > self.today:
                return uposatha
        # TODO: Raise exception.
        return None

    def today_is_uposatha(self):
        for uposatha in self.get_uposathas():
            if uposatha.date == self.today:
                return True
        return False

    def get_uposathas(self):
        return [an_event for an_event in self.events if an_event.is_uposatha()]

    def days_to_next_uposatha(self):
        td = self.next_uposatha().date - self.today
        return td.days

    def events_in_year(self, year):
        return [e for e in self.events if e.date.year == year]

    def special_days_in_year(self, year):
        return [e for e in self.events_in_year(year) if e.special_day]

    def uposathas_in_year(self, year):
        in_year = []
        for event in self.events:
            if event.is_uposatha():
                if event.date.year == year:
                    in_year.append(event)

        return in_year

    def seasons_in_year(self, year):
        seasons_in_year = []
        for season in self.seasons:
            if season.end_date().year == year:
                seasons_in_year.append(season)
        return seasons_in_year

    def start_of_rains(self):
        for season in self.seasons:
            if season.season_name == "Gimha":
                if season.events[0].date.year == self.today.year:
                    return season.end_date() + datetime.timedelta(1)
        return None

    def long_hot_seasons(self):
        years = []
        for event_ in self.events:
            if event_.uposatha_of_season == 10:
                years.append(event_.date.year)

        return years

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
        # TODO: make private
        self.summaries = [details["summary"]]

        self.moon_name = ""
        self.special_day = ""
        self.vassa_day = ""

        self.uposatha_of_season = 0
        self.uposatha_days = 0

        self.phase_names = ["Full", "Waning", "New", "Waxing"]
        self.special_days = ["Āsāḷha Pūjā", "Māgha Pūjā", "Pavāraṇā Day", "Visākha Pūjā"]
        self.vassa_days = ["First day of Vassa", "Last day of Vassa"]

        self._extended_summary = None
        self.season = None

    def add_details(self, details):
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
                self._extended_summary = ExtendedSummary(summary)

    def complete(self):
        self._set_moon_phase()
        self._set_special_days()
        self._set_vassa_days()
        self._set_extended_summary()

        if self._extended_summary:
            self.uposatha_of_season = self._extended_summary.uposatha_of_season()
            self.uposatha_days = self._extended_summary.uposatha_days()

    def is_uposatha(self):
        return self.moon_name in ["Full", "New"]

    def is_end_of_season(self):
        if self.moon_name != "Full":
            return False

        season_info = self._extended_summary

        if season_info.uposatha_of_season() == season_info.uposatha_of_season():
            return True

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
        if self._extended_summary:
            outstr += " : Uposatha # {}".format(self.uposatha_of_season)
            outstr += " : Uposatha Days {}".format(self.uposatha_days)
        return outstr


class ExtendedSummary:
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

    def uposatha_of_season(self):
        numbers = re.findall("[0-9]+", self.summary)
        return int(numbers[1])
        # TODO: Throw exception if not 3 numbers.

    def uposathas_in_season(self):
        numbers = re.findall("[0-9]+", self.summary)
        return int(numbers[2])
        # TODO: Throw exception if not 3 numbers.


class Season:
    """
    Representation of a season in the calendar including events
    for that period.
    """
    def __init__(self):
        self.season_name = ""
        self.uposatha_count = 0
        self.events = []

    def end_date(self):
        return self.events[-1].date

    def english_name(self):
        translation = {
            "Hemanta": "Cold",
            "Gimha": "Hot",
            "Vassāna": "Rainy"
        }
        return translation[self.season_name]

    @property
    def uposathas(self):
        return [event for event in self.events if event.moon_name in ["Full", "New"]]

    @property
    def half_moons(self):
        return [event for event in self.events if event.moon_name in ["Waning", "Waxing"]]

    @property
    def start_year(self):
        return self.events[0].date.year

    @property
    def end_year(self):
        return self.events[-1].date.year

    def __str__(self):
        event_count = len(self.events)
        return "Season: {}, {} uposathas, {} events".format(self.season_name, self.uposatha_count, event_count)


class SeasonMaker:
    """
    Generates a list of Seasons from a list of Events.

    """
    def __init__(self, events):
        # This is pretty ugly - only first vassa day falls on a non-moon day.
        self._events = [event for event in events if event.moon_name != "None"]
        self._trim_events()
        self._next_season = Season()
        self._seasons = []


    def _trim_events(self):
        """
        The whole process is much easier if we delete the following:

        The first event when it is an uposatha.
        The last event if it is a not an uposatha.

        Then all we need to do is process the pairs. It is pretty unlikely that
        we'll want the details of those specific uposathas as they are long in the
        past or future. Anyway, I'm gonna rewrite the whole thing anyway.
        """

        if not self._events:
            # TODO Raise error.
            return

        if self._events[0].is_uposatha():
            del self._events[0]

        if not self._events[-1].is_uposatha():
            del self._events[-1]

    def _season_has_changed(self, uposatha):
        """
        Check if the next uposatha belongs to a different season.

        :param uposatha: The next uposatha.
        :return: True if uposatha belongs to different season.
        """
        old = self._next_season.season_name

        # First season not initialised.
        if not old: return False

        new = uposatha._extended_summary.season_name()
        return old != new

    def _add_half_month(self, half_moon: Event, uposatha: Event):
        """
        Take two consecutive events and add them to a season.

        As seasons end on a full moon we can be sure that these two events
        belong to the same season. The half moon will not have extended
        details so season must be determined from the following uposatha.

        :param half_moon: A waxing or waning moon
        :param uposatha: The full or new moon following the half moon.
        """

        if self._season_has_changed(uposatha):
            self._seasons.append(self._next_season)
            self._next_season = Season()

        season_info = uposatha._extended_summary

        self._next_season.season_name = season_info.season_name()
        self._next_season.uposatha_count = season_info.uposathas_in_season()
        self._next_season.events.append(half_moon)
        self._next_season.events.append(uposatha)
        half_moon.season = self._next_season
        uposatha.season = self._next_season

    def get_seasons(self):
        """
        Use the list of events to create a list of seasons.

        At this point _trim_events() has been called so we can
        assume _events is a list of pairs of half_moons and uposathas.

        :return: The list of seasons.
        """

        event_iter = iter(self._events)

        for half_moon_event in event_iter:
            uposatha_event = next(event_iter)
            self._add_half_month(half_moon_event, uposatha_event)

        # Add the final season, complete or not.
        self._seasons.append(self._next_season)

        return self._seasons

if __name__ == '__main__':
    with open("mahanikaya.ical", "r") as f:
        content = f.read()

    ical = icalendar.Calendar.from_ical(content)
    calendar = MahanikayaCalendar()
    calendar.import_ical(ical)

    print("Number of events: {}".format(len(calendar.events)))

    print("First 12 events")
    for event in calendar.events[0:12]:
        print(event)

    print("Pavaranas")
    pavaranas = [event for event in calendar.events if event.special_day == "Pavāraṇā Day"]
    for pavarana in pavaranas:
        print(pavarana)

    print("Last event")
    print(calendar.events[-1])