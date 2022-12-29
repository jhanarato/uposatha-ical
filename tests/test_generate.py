from datetime import date

import pytest

from generate import uposatha_lengths, generate_event, generate_season_with_one_event
from generate import generate_uposatha_dates

def test_uposatha_lengths():
    assert list(uposatha_lengths()) == [15, 15, 14, 15, 15, 15, 14, 15]

def test_generate_event():
    event = generate_event(on_date=date(2022, 12, 29))
    assert event.date == date(2022, 12, 29)

def test_generate_season_with_one_event():
    season = generate_season_with_one_event(event_date=date(2022, 12, 29))
    assert len(season.events) == 1

def test_generate_first_uposatha_date():
    dates = list(generate_uposatha_dates(day_before_season=date(2022, 12, 29)))
    assert dates[0] == date(2023, 1, 13)

def test_generate_eight_uposathas():
    dates = list(generate_uposatha_dates(day_before_season=date(2022, 12, 29)))
    assert len(dates) == 8