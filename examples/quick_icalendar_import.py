import icalendar
from forest_sangha_moons.MahanikayaCalendar import MahanikayaCalendar

def import_calendar():
    """ For use in python console. Quickly import the icalendar file for exploration """
    with open("mahanikaya.ical", "r") as f:
        content = f.read()

    ical = icalendar.Calendar.from_ical(content)
    calendar = MahanikayaCalendar()
    calendar.import_ical(ical)
    return calendar