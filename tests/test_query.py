from datetime import date
import pytest

@pytest.mark.parametrize("today,is_uposatha",
                         [
                             (date(2010, 11, 29), False),
                             (date(2010, 12, 6), True),
                             (date(2010, 12, 14), False),
                             (date(2010, 12, 21), True),
                             # Events out of calendar range
                             (date(2009, 1, 1), False),
                             (date(2011, 1, 1), False)
                          ])
def test_today_is_uposatha(today, is_uposatha, one_month_of_events):
    one_month_of_events.today = today
    assert one_month_of_events.today_is_uposatha() == is_uposatha

@pytest.mark.parametrize("today,days_to_next",
                         [
                             (date(2010, 12, 5), 1),
                             (date(2010, 12, 6), 15)
                          ])
def test_days_to_next_uposatha(today, days_to_next, one_month_of_events):
    one_month_of_events.today = today
    assert one_month_of_events.days_to_next_uposatha() == days_to_next

def test_first_day_of_rains_this_year(calendar_2010_10_24):
    calendar_2010_10_24.today = date(2011, 1, 1)
    assert calendar_2010_10_24.start_of_rains() == date(2011, 7, 16)

@pytest.mark.skip(reason="event.uposatha_in_seaons is not set in calendar generation")
def test_long_hot_seasons(calendar_2010_10_24):
    assert calendar_2010_10_24.long_hot_seasons() == [ 2012 ]
