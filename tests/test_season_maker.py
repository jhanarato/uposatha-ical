from datetime import date
from forest_sangha_moons.MahanikayaCalendar import MahanikayaCalendar, SeasonMaker
from conftest import details_to_events

def test_trim_events():
    trim_half_from_front = {"date": date(2010, 1, 15), "summary": "New Moon - 15 day Hemanta 5/8"}
    keep_half_moon = {"date": date(2010, 1, 23), "summary": "Waxing Moon"}
    keep_uposatha = {"date": date(2010, 1, 30), "summary": "Full Moon - 15 day Hemanta 6/8"}
    trim_half_from_end = {"date": date(2010, 2, 7), "summary": "Waning Moon"}

    details = [trim_half_from_front, keep_half_moon, keep_uposatha, trim_half_from_end]

    events_to_trim = details_to_events(details)

    maker = SeasonMaker(events_to_trim)
    maker._trim_events()

    assert len(maker._events) == 2

    half_moon = maker._events[0]
    uposatha = maker._events[1]

    assert half_moon.moon_name == "Waxing"
    assert uposatha.moon_name == "Full"

def test_nothing_to_trim():
    half_moon = {"date": date(2010, 1, 23), "summary": "Waxing Moon"}
    uposatha = {"date": date(2010, 1, 30), "summary": "Full Moon - 15 day Hemanta 6/8"}

    details = [half_moon, uposatha]

    events_no_trim = details_to_events(details)

    maker = SeasonMaker(events_no_trim)
    maker._trim_events()

    assert len(maker._events) == 2

    half_moon = maker._events[0]
    uposatha = maker._events[1]

    assert half_moon.moon_name == "Waxing"
    assert uposatha.moon_name == "Full"

def test_add_half_month():
    half_detail = {"date": date(2010, 1, 8), "summary": "Waning Moon"}
    uposatha_detail = {"date": date(2010, 1, 15), "summary": "New Moon - 15 day Hemanta 5/8"}

    cal = MahanikayaCalendar()
    cal._process_details(half_detail)
    cal._process_details(uposatha_detail)
    cal._complete_event()

    assert len(cal.events) == 2

    half_event = cal.events[0]
    uposatha_event = cal.events[1]

    maker = SeasonMaker([])

    maker._add_half_month(half_event, uposatha_event)

    season = maker._next_season

    assert season.season_name == "Hemanta"
    assert season.uposatha_count == 8
    assert len(season.events) == 2
    assert season.events[0].moon_name == "Waning"
    assert season.events[1].moon_name == "New"

def test_season_has_changed():
    first_uposatha_detail = {"date": date(2010, 12, 6), "summary": "New Moon - 15 day Hemanta 1/8"}

    events = details_to_events([first_uposatha_detail])

    assert len(events) == 1

    first_uposatha_event = events[0]

    maker = SeasonMaker([])
    maker._next_season.season_name = "Vassāna"
    assert maker._season_has_changed(first_uposatha_event)

def test_season_not_initialised():
    # For the very first event, we have a new Season without
    # any content.
    detail = {"date": date(2010, 12, 6), "summary": "New Moon - 15 day Hemanta 1/8"}
    event = details_to_events([detail])[0]
    maker = SeasonMaker([])
    assert not maker._season_has_changed(event)

def test_two_pairs_same_season():
    details = [
        {"date": date(2010, 11, 29), "summary": "Waning Moon"},
        {"date": date(2010, 12, 6), "summary": "New Moon - 15 day Hemanta 1/8"},
        {"date": date(2010, 12, 14), "summary": "Waxing Moon"},
        {"date": date(2010, 12, 21), "summary": "Full Moon - 15 day Hemanta 2/8"}
    ]

    two_pairs_of_events = details_to_events(details)
    assert len(two_pairs_of_events) == 4

    maker = SeasonMaker(two_pairs_of_events)
    seasons = maker.get_seasons()

    assert len(seasons) == 1
    assert seasons[0].season_name == "Hemanta"

def test_two_pairs_different_season():
    details = [
        {"date": date(2010, 2, 21), "summary": "Waxing Moon"},
        {"date": date(2010, 2, 28), "summary": "Full Moon - 15 day Hemanta 8/8"},
        {"date": date(2010, 2, 28), "summary": "Māgha Pūjā"},
        {"date": date(2010, 3, 8), "summary": "Waning Moon"},
        {"date": date(2010, 3, 15), "summary": "New Moon - 15 day Gimha 1/10"}
    ]

    two_seasons = details_to_events(details)

    maker = SeasonMaker(two_seasons)
    seasons = maker.get_seasons()

    assert len(seasons) == 2

    assert seasons[0].season_name == "Hemanta"
    assert seasons[1].season_name == "Gimha"

