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

