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