from datetime import date, timedelta
from forest_sangha_moons.MahanikayaCalendar import MahanikayaCalendar, Season, Event

def uposatha_lengths():
    fourteen_days = [3, 7]
    for number in range(1, 9):
        if number in fourteen_days:
            yield 14
        else:
            yield 15

def add_month(lengths):
    for length in lengths:
        yield length
    yield 15
    yield 15

def is_long(year, season_name):
    long_years = [2012]
    return season_name == "Gimha" and year in long_years

def generate_event(on_date):
    details = {"date": on_date, "summary": ""}
    event = Event(details)
    return event

def generate_season_with_one_event(event_date):
    rainy = Season()
    rainy.season_name = "Vassāna"
    rainy.events = [generate_event(event_date)]
    return rainy

def generate_uposatha_dates(day_before_season, long_hot=False):
    lengths = iter(uposatha_lengths())
    if long_hot:
        lengths = add_month(lengths)

    next_date = day_before_season + timedelta(days=next(lengths))

    yield next_date

    for length in lengths:
        next_date += timedelta(days=length)
        yield next_date

def generate_events_for_season(day_before_season, long_hot=False):
    events = []
    for event_date in generate_uposatha_dates(day_before_season, long_hot):
        event = generate_event(event_date)
        events.append(event)

    return events

def generate_season(day_before_season, season_name):
    long_hot = is_long(day_before_season.year, season_name)
    season = Season()
    season.season_name = season_name
    season.events = generate_events_for_season(day_before_season, long_hot)
    return season

def generate_season_after_season(season):
    name_after = {"Gimha": "Vassāna",
                    "Vassāna": "Hemanta",
                    "Hemanta": "Gimha"}

    day_before_season = season.events[-1].date
    name = name_after[season.season_name]

    return generate_season(day_before_season, name)

def generate_calendar(day_before_calendar, first_season_name, number_of_seasons):
    calendar = MahanikayaCalendar()

    season = generate_season(day_before_calendar, first_season_name)
    calendar.seasons.append(season)

    for _ in range(1, number_of_seasons):
        season = generate_season_after_season(season)
        calendar.seasons.append(season)

    return calendar
