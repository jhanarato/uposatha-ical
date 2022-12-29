from datetime import date

from generate import uposatha_lengths, generate_event

def test_uposatha_lengths():
    assert uposatha_lengths() == [15, 15, 14, 15, 15, 15, 14, 15]

def test_generate_event():
    event = generate_event(date(2022, 12, 29))
    assert event.date == date(2022, 12, 29)