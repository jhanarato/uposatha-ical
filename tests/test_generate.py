import datetime
from datetime import date

import pytest

from generate import uposatha_lengths, generate_event, generate_season_with_one_event
from generate import generate_uposatha_dates, generate_events_for_season
from generate import generate_season, generate_season_after_season
from generate import generate_calendar, add_month, is_long

def test_uposatha_lengths():
    assert list(uposatha_lengths()) == [15, 15, 14, 15, 15, 15, 14, 15]

def test_generate_event():
    event = generate_event(on_date=date(2022, 12, 29))
    assert event.date == date(2022, 12, 29)

def test_generate_season_with_one_event():
    season = generate_season_with_one_event(event_date=date(2022, 12, 29))
    assert len(season.events) == 1

@pytest.fixture
def uposatha_dates():
    return list(generate_uposatha_dates(day_before_season=date(2022, 12, 29)))

def test_generate_first_uposatha_date(uposatha_dates):
    assert uposatha_dates[0] == date(2023, 1, 13)

def test_generate_eight_uposathas(uposatha_dates):
    assert len(uposatha_dates) == 8

@pytest.mark.parametrize(
    "position,date_at_position", [
        (0, date(2023, 1, 13)),
        (1, date(2023, 1, 28)),
        (2, date(2023, 2, 11)),
        (3, date(2023, 2, 26)),
        (4, date(2023, 3, 13)),
        (5, date(2023, 3, 28)),
        (6, date(2023, 4, 11)),
        (7, date(2023, 4, 26))
    ]
)
def test_generate_correct_uposatha_dates(position, date_at_position, uposatha_dates):
    assert uposatha_dates[position] == date_at_position

def test_generate_events_for_season():
    events = generate_events_for_season(day_before_season=date(2022, 12, 29))
    assert len(events) == 8

def test_last_day_of_events_generated():
    event = generate_events_for_season(day_before_season=date(2022, 12, 29))[7]
    assert event.date == date(2023, 4, 26)

def test_generate_season():
    season = generate_season(date(2010, 7, 26), "Vassāna")
    assert season.season_name == "Vassāna"
    assert len(season.events) == 8

def test_generate_season_name():
    season = generate_season(date(2010, 7, 26), "Gimha")
    next_season = generate_season_after_season(season)
    assert next_season.season_name == "Vassāna"

def test_generate_season_date():
    season = generate_season(date(2010, 7, 26), "Gimha")
    next_season = generate_season_after_season(season)

    last_event = season.events[-1]
    first_event = next_season.events[0]
    difference = (first_event.date - last_event.date).days
    assert difference == 15

def test_generate_calendar_with_one_season():
    calendar = generate_calendar(date(2022, 4, 1), "Gimha", 1)
    assert len(calendar.seasons) == 1

def test_generate_calendar_with_three_seasons():
    calendar = generate_calendar(date(2022, 4, 1), "Gimha", 3)
    assert len(calendar.seasons) == 3

def test_generate_seasons_names():
    calendar = generate_calendar(date(2022, 4, 1), "Gimha", 3)
    names = [season.season_name for season in calendar.seasons]
    assert names == ["Gimha", "Vassāna", "Hemanta"]

def test_add_month_to_uposatha_lengths():
    with_extra_month = list(add_month(uposatha_lengths()))
    assert with_extra_month == [15, 15, 14, 15, 15, 15, 14, 15, 15, 15]

@pytest.mark.parametrize(
    "year,name,long",
    [
        (2012, "Gimha", True),
        (2011, "Gimha", False),
        (2012, "Vassāna", False)
    ]
)
def test_is_long_hot_season(year, name, long):
    assert is_long(2012, "Gimha")
