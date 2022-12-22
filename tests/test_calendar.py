from datetime import date

from forest_sangha_moons.MahanikayaCalendar import MahanikayaCalendar

def test_x(x):
    assert x == "x"

def test_one_detail():
    waxing_detail = {"date": date(2022, 3, 18), "summary": "Waxing Moon"}

    cal = MahanikayaCalendar()

    assert not cal._incomplete_event

    cal._process_details(waxing_detail)

    assert len(cal._incomplete_event.summaries) == 1
    assert cal._incomplete_event.summaries[0] == "Waxing Moon"
