from datetime import date

from forest_sangha_moons.MahanikayaCalendar import MahanikayaCalendar

from conftest import initialise_calendar

def test_one_detail():
    waxing_detail = {"date": date(2022, 3, 18), "summary": "Waxing Moon"}

    cal = MahanikayaCalendar()

    assert not cal._incomplete_event

    cal._process_details(waxing_detail)

    assert len(cal._incomplete_event.summaries) == 1
    assert cal._incomplete_event.summaries[0] == "Waxing Moon"

def test_two_details_same_date():
    full_detail = {"date": date(2022, 3, 18), "summary": "Full Moon - 15 day Hemanta 6/8"}
    special_detail = {"date": date(2022, 3, 18), "summary": "Āsāḷha Pūjā"}

    cal = MahanikayaCalendar()
    cal._process_details(full_detail)
    cal._process_details(special_detail)

    assert len(cal._incomplete_event.summaries) == 2

def test_two_events():
    waxing_detail = {"date": date(2022, 3, 18), "summary": "Waxing Moon"}
    full_detail = {"date": date(2022, 3, 19), "summary": "Full Moon - 15 day Hemanta 6/8"}

    cal = MahanikayaCalendar()
    cal._process_details(waxing_detail)
    cal._process_details(full_detail)

    assert len(cal.events) == 1

    complete = cal.events[0]

    assert len(complete.summaries) == 1
    assert complete.moon_name == "Waxing"

    incomplete = cal._incomplete_event

    assert len(incomplete.summaries) == 1
    assert incomplete.moon_name == ""

def test_date_has_changed():
    waxing_detail = {"date": date(2022, 3, 18), "summary": "Waxing Moon"}
    full_detail = {"date": date(2022, 3, 19), "summary": "Full Moon - 15 day Hemanta 6/8"}

    cal = MahanikayaCalendar()
    cal._process_details(waxing_detail)

    assert cal._new_date(full_detail)

def test_next_event():
    details = [
        {"date": date(2010, 11, 29), "summary": "Waning Moon"},
        {"date": date(2010, 12, 6), "summary": "New Moon - 15 day Hemanta 1/8"},
        {"date": date(2010, 12, 14), "summary": "Waxing Moon"},
        {"date": date(2010, 12, 21), "summary": "Full Moon - 15 day Hemanta 2/8"}
    ]

    cal = initialise_calendar(details)

    cal.today = date(2010, 12, 14)

    next_event = cal.next_event()

    assert next_event.date == date(2010, 12, 21)

def test_next_uposatha():
    details = [
        {"date": date(2010, 11, 29), "summary": "Waning Moon"},
        {"date": date(2010, 12, 6), "summary": "New Moon - 15 day Hemanta 1/8"},
        {"date": date(2010, 12, 14), "summary": "Waxing Moon"},
        {"date": date(2010, 12, 21), "summary": "Full Moon - 15 day Hemanta 2/8"}
    ]

    cal = initialise_calendar(details)

    cal.today = date(2010, 12, 5)
    uposatha = cal.next_uposatha()
    assert uposatha.date == date(2010, 12, 6)


    cal.today = date(2010, 12, 6)
    uposatha = cal.next_uposatha()
    assert uposatha.date == date(2010, 12, 21)

def test_is_uposatha():
    details = [
        {"date": date(2010, 11, 29), "summary": "Waning Moon"},
        {"date": date(2010, 12, 6), "summary": "New Moon - 15 day Hemanta 1/8"},
        {"date": date(2010, 12, 14), "summary": "Waxing Moon"},
        {"date": date(2010, 12, 21), "summary": "Full Moon - 15 day Hemanta 2/8"}
    ]

    cal = initialise_calendar(details)

    # Normal usage
    cal.today = date(2010, 11, 29)
    assert not cal.today_is_uposatha()

    cal.today = date(2010, 12, 6)
    assert cal.today_is_uposatha()

    cal.today = date(2010, 12, 14)
    assert not cal.today_is_uposatha()

    cal.today = date(2010, 12, 21)
    assert cal.today_is_uposatha()

    # Before range of events.
    cal.today = date(2009, 1, 1)
    assert not cal.today_is_uposatha()

    # After range of events.
    cal.today = date(2011, 1, 1)
    assert not cal.today_is_uposatha()

def test_get_uposathas():
    details = [
        {"date": date(2010, 11, 29), "summary": "Waning Moon"},
        {"date": date(2010, 12, 6), "summary": "New Moon - 15 day Hemanta 1/8"},
        {"date": date(2010, 12, 14), "summary": "Waxing Moon"},
        {"date": date(2010, 12, 21), "summary": "Full Moon - 15 day Hemanta 2/8"}
    ]

    cal = initialise_calendar(details)
    uposathas = cal.get_uposathas()
    assert len(uposathas) == 2
    assert uposathas[0].moon_name == "New"
    assert uposathas[1].moon_name == "Full"
    