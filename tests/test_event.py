from datetime import date

from forest_sangha_moons.MahanikayaCalendar import Event

def test_set_moon_phase():
    waxing_detail = {"date": date(2022, 3, 18), "summary": "Waxing Moon"}
    event = Event(waxing_detail)
    event._set_moon_phase()
    assert event.moon_name == "Waxing"

    waning_detail = {"date": date(2022, 3, 18), "summary": "Waning Moon"}
    event = Event(waning_detail)
    event._set_moon_phase()
    assert event.moon_name == "Waning"

    full_detail = {"date": date(2022, 3, 18), "summary": "Full Moon - 15 day Hemanta 6/8"}
    event = Event(full_detail)
    event._set_moon_phase()
    assert event.moon_name == "Full"

    new_detail = {"date": date(2022, 3, 18), "summary": "New Moon - 15 day Hemanta 5/8"}
    event = Event(new_detail)
    event._set_moon_phase()
    assert event.moon_name == "New"

    vassa_first_day_detail = {"date": date(2022, 3, 18), "summary": "First day of Vassa"}
    event = Event(vassa_first_day_detail)
    event._set_moon_phase()
    assert event.moon_name == "None"

def test_set_special_day():
    # Every special day falls on a full moon day.
    full_detail = {"date": date(2022, 3, 18), "summary": "Full Moon - 15 day Hemanta 6/8"}
    special_detail = {"date": date(2022, 3, 18), "summary": "Āsāḷha Pūjā"}
    event = Event(full_detail)
    event.add_details(special_detail)
    event._set_moon_phase()
    event._set_special_days()
    assert event.special_day == "Āsāḷha Pūjā"

def test_set_first_vassa():
    # The first day of vassa is not a moon day.
    detail = {"date": date(2022, 3, 18), "summary": "First day of Vassa"}
    event = Event(detail)
    event._set_vassa_days()
    assert event.vassa_day == "First day of Vassa"

def test_set_last_vassa_day():
    # The only day with three summaries is the end of the rains.
    full_detail = {"date": date(2022, 3, 18), "summary": "Full Moon - 15 day Hemanta 6/8"}
    special_detail = {"date": date(2022, 3, 18), "summary": "Pavāraṇā Day"}
    last_detail = {"date": date(2022, 3, 18), "summary": "Last day of Vassa"}

    event = Event(full_detail)
    event.add_details(special_detail)
    event.add_details(last_detail)

    event._set_vassa_days()
    assert event.vassa_day == "Last day of Vassa"

def test_complete():
    full_detail = {"date": date(2022, 3, 18), "summary": "Full Moon - 15 day Hemanta 6/8"}
    special_detail = {"date": date(2022, 3, 18), "summary": "Pavāraṇā Day"}
    last_detail = {"date": date(2022, 3, 18), "summary": "Last day of Vassa"}

    event = Event(full_detail)
    event.add_details(special_detail)
    event.add_details(last_detail)

    event.complete()

    assert event.moon_name == "Full"
    assert event.special_day == "Pavāraṇā Day"
    assert event.vassa_day == "Last day of Vassa"

def test_set_extended_summary():
    full_detail = {"date": date(2022, 3, 18), "summary": "Full Moon - 15 day Hemanta 6/8"}

    event = Event(full_detail)
    event.complete()

    season = event._extended_summary.season_name()
    assert season == "Hemanta"

def test_is_uposatha():
    waxing_detail = {"date": date(2022, 3, 18), "summary": "Waxing Moon"}
    full_detail = {"date": date(2022, 3, 18), "summary": "Full Moon - 15 day Hemanta 6/8"}
    waning_detail = {"date": date(2022, 3, 18), "summary": "Waning Moon"}
    new_detail = {"date": date(2022, 3, 18), "summary": "New Moon - 15 day Hemanta 5/8"}

    waxing_event = Event(waxing_detail)
    full_event = Event(full_detail)
    waning_event = Event(waning_detail)
    new_event = Event(new_detail)

    waxing_event.complete()
    full_event.complete()
    waning_event.complete()
    new_event.complete()

    assert not waxing_event.is_uposatha()
    assert not waning_event.is_uposatha()

    assert full_event.is_uposatha()
    assert new_event.is_uposatha()

def test_is_end_of_season():
    half_moon_detail = {"date": date(2010, 7, 19), "summary": "Waxing Moon"}
    uposatha_end_detail = {"date": date(2010, 7, 26), "summary": "Full Moon - 15 day Gimha 10/10"}
    uposatha_not_end_detail = {"date": date(2010, 8, 10), "summary": "New Moon - 15 day Vassāna 1/8"}

    half_moon_event = Event(half_moon_detail)
    uposatha_end_event = Event(uposatha_end_detail)
    uposatha_not_end_event = Event(uposatha_not_end_detail)

    half_moon_event.complete()
    uposatha_end_event.complete()
    uposatha_not_end_event.complete()

    assert not half_moon_event.is_end_of_season()
    assert not uposatha_not_end_event.is_end_of_season()
    assert uposatha_end_event.is_end_of_season()