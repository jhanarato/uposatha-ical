from datetime import date
from forest_sangha_moons.MahanikayaCalendar import Season, Event

def uposatha_lengths():
    lengths = []
    for number in range(1, 9):
        if number == 3 or number == 7:
            lengths.append(14)
        else:
            lengths.append(15)

    return lengths

def generate_event(on_date):
    details = {"date": on_date, "summary": ""}
    event = Event(details)
    return event

def generate_season_with_one_event(event_date):
    rainy = Season()
    rainy.season_name = "Vassāna"
    rainy.events = [generate_event(event_date)]
    return rainy