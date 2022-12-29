from datetime import date, timedelta
from forest_sangha_moons.MahanikayaCalendar import Season, Event

def uposatha_lengths():
    for number in range(1, 9):
        if number == 3 or number == 7:
            yield 14
        else:
            yield 15

def generate_event(on_date):
    details = {"date": on_date, "summary": ""}
    event = Event(details)
    return event

def generate_season_with_one_event(event_date):
    rainy = Season()
    rainy.season_name = "Vassāna"
    rainy.events = [generate_event(event_date)]
    return rainy

def generate_uposatha_dates(day_before_season):
    dates = []
    lengths = list(uposatha_lengths())
    next_date = day_before_season + timedelta(days=lengths[0])
    dates.append(next_date)
    for length in lengths[1:]:
        next_date += timedelta(days=length)
        dates.append(next_date)
    return dates
