from datetime import date, timedelta
from forest_sangha_moons.MahanikayaCalendar import Season, Event

def uposatha_lengths():
    fourteen_days = [3, 7]
    for number in range(1, 9):
        if number in fourteen_days:
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
    lengths = iter(uposatha_lengths())
    next_date = day_before_season + timedelta(days=next(lengths))
    yield next_date
    for length in lengths:
        next_date += timedelta(days=length)
        yield next_date
