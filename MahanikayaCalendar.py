class MahanikayaCalendar:
    def __init__(self, ical):
        self._events = []

        for component in ical.walk():
            summary = component.get('SUMMARY')
            dtstart = component.get('DTSTART')
            if summary != None and dtstart != None:
                event_description = summary
                event_date = dtstart.dt
                self._events.append((event_description, event_date))

    def number_of_events(self):
        return len(self._events)