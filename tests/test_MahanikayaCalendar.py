from unittest import TestCase
from datetime import date

from conftest import details_to_seasons, details_to_events, initialise_calendar
from forest_sangha_moons.MahanikayaCalendar import Event, Season, ExtendedSummary, SeasonMaker, MahanikayaCalendar

def test_x(x):
    assert x == "x"


class TestMahaNikayaCalendar(TestCase):

    def test_one_detail(self):
        waxing_detail = {"date": date(2022, 3, 18), "summary": "Waxing Moon"}

        cal = MahanikayaCalendar()
        self.assertIsNone(cal._incomplete_event)

        cal._process_details(waxing_detail)

        self.assertEqual(1, len(cal._incomplete_event.summaries))
        self.assertEqual("Waxing Moon", cal._incomplete_event.summaries[0])

    def test_two_details_same_date(self):
        full_detail = {"date": date(2022, 3, 18), "summary": "Full Moon - 15 day Hemanta 6/8"}
        special_detail = {"date": date(2022, 3, 18), "summary": "Āsāḷha Pūjā"}

        cal = MahanikayaCalendar()
        cal._process_details(full_detail)
        cal._process_details(special_detail)

        self.assertEqual(2, len(cal._incomplete_event.summaries))

    def test_two_events(self):
        waxing_detail = {"date": date(2022, 3, 18), "summary": "Waxing Moon"}
        full_detail = {"date": date(2022, 3, 19), "summary": "Full Moon - 15 day Hemanta 6/8"}

        cal = MahanikayaCalendar()
        cal._process_details(waxing_detail)
        cal._process_details(full_detail)

        self.assertEqual(1, len(cal.events))

        complete = cal.events[0]

        self.assertEqual(1, len(complete.summaries))
        self.assertEqual("Waxing", complete.moon_name)

        incomplete = cal._incomplete_event

        self.assertEqual(1, len(incomplete.summaries))
        self.assertEqual("", incomplete.moon_name)

    def test_date_has_changed(self):
        waxing_detail = {"date": date(2022, 3, 18), "summary": "Waxing Moon"}
        full_detail = {"date": date(2022, 3, 19), "summary": "Full Moon - 15 day Hemanta 6/8"}

        cal = MahanikayaCalendar()
        cal._process_details(waxing_detail)
        self.assertTrue(cal._new_date(full_detail))

    def test_next_event(self):
        details = [
            {"date": date(2010, 11, 29), "summary": "Waning Moon"},
            {"date": date(2010, 12, 6), "summary": "New Moon - 15 day Hemanta 1/8"},
            {"date": date(2010, 12, 14), "summary": "Waxing Moon"},
            {"date": date(2010, 12, 21), "summary": "Full Moon - 15 day Hemanta 2/8"}
        ]

        cal = initialise_calendar(details)

        cal.today = date(2010, 12, 14)

        next_event = cal.next_event()

        self.assertEqual(date(2010, 12, 21), next_event.date)

    def test_next_uposatha(self):
        details = [
            {"date": date(2010, 11, 29), "summary": "Waning Moon"},
            {"date": date(2010, 12, 6), "summary": "New Moon - 15 day Hemanta 1/8"},
            {"date": date(2010, 12, 14), "summary": "Waxing Moon"},
            {"date": date(2010, 12, 21), "summary": "Full Moon - 15 day Hemanta 2/8"}
        ]

        cal = initialise_calendar(details)

        cal.today = date(2010, 12, 5)
        uposatha = cal.next_uposatha()
        self.assertEqual(date(2010, 12, 6), uposatha.date)


        cal.today = date(2010, 12, 6)
        uposatha = cal.next_uposatha()
        self.assertEqual(date(2010, 12, 21), uposatha.date)


    def test_is_uposatha(self):
        details = [
            {"date": date(2010, 11, 29), "summary": "Waning Moon"},
            {"date": date(2010, 12, 6), "summary": "New Moon - 15 day Hemanta 1/8"},
            {"date": date(2010, 12, 14), "summary": "Waxing Moon"},
            {"date": date(2010, 12, 21), "summary": "Full Moon - 15 day Hemanta 2/8"}
        ]

        cal = initialise_calendar(details)

        # Normal usage
        cal.today = date(2010, 11, 29)
        self.assertFalse(cal.today_is_uposatha())
        cal.today = date(2010, 12, 6)
        self.assertTrue(cal.today_is_uposatha())
        cal.today = date(2010, 12, 14)
        self.assertFalse(cal.today_is_uposatha())
        cal.today = date(2010, 12, 21)
        self.assertTrue(cal.today_is_uposatha())

        # Before range of events.
        cal.today = date(2009, 1, 1)
        self.assertFalse(cal.today_is_uposatha())

        # After range of events.
        cal.today = date(2011, 1, 1)
        self.assertFalse(cal.today_is_uposatha())

    def test_get_uposathas(self):
        details = [
            {"date": date(2010, 11, 29), "summary": "Waning Moon"},
            {"date": date(2010, 12, 6), "summary": "New Moon - 15 day Hemanta 1/8"},
            {"date": date(2010, 12, 14), "summary": "Waxing Moon"},
            {"date": date(2010, 12, 21), "summary": "Full Moon - 15 day Hemanta 2/8"}
        ]

        cal = initialise_calendar(details)
        uposathas = cal.get_uposathas()
        self.assertEqual(2, len(uposathas))
        self.assertEqual("New", uposathas[0].moon_name)
        self.assertEqual("Full", uposathas[1].moon_name)

class TestSeasonMaker(TestCase):
    def test_trim_events(self):
        trim_half_from_front = {"date": date(2010, 1, 15), "summary": "New Moon - 15 day Hemanta 5/8"}
        keep_half_moon = {"date": date(2010, 1, 23), "summary": "Waxing Moon"}
        keep_uposatha = {"date": date(2010, 1, 30), "summary": "Full Moon - 15 day Hemanta 6/8"}
        trim_half_from_end = {"date": date(2010, 2, 7), "summary": "Waning Moon"}

        details = [trim_half_from_front, keep_half_moon, keep_uposatha, trim_half_from_end]

        events_to_trim = details_to_events(details)

        maker = SeasonMaker(events_to_trim)
        maker._trim_events()

        self.assertEqual(2, len(maker._events))

        half_moon = maker._events[0]
        uposatha = maker._events[1]

        self.assertEqual("Waxing", half_moon.moon_name)
        self.assertEqual("Full", uposatha.moon_name)

    def test_nothing_to_trim(self):
        half_moon = {"date": date(2010, 1, 23), "summary": "Waxing Moon"}
        uposatha = {"date": date(2010, 1, 30), "summary": "Full Moon - 15 day Hemanta 6/8"}

        details = [half_moon, uposatha]

        events_no_trim = details_to_events(details)

        maker = SeasonMaker(events_no_trim)
        maker._trim_events()

        self.assertEqual(2, len(maker._events))

        half_moon = maker._events[0]
        uposatha = maker._events[1]

        self.assertEqual("Waxing", half_moon.moon_name)
        self.assertEqual("Full", uposatha.moon_name)

    def test_add_half_month(self):
        half_detail = {"date": date(2010, 1, 8), "summary": "Waning Moon"}
        uposatha_detail = {"date": date(2010, 1, 15), "summary": "New Moon - 15 day Hemanta 5/8"}

        cal = MahanikayaCalendar()
        cal._process_details(half_detail)
        cal._process_details(uposatha_detail)
        cal._complete_event()

        self.assertEqual(2, len(cal.events))

        half_event = cal.events[0]
        uposatha_event = cal.events[1]

        maker = SeasonMaker([])

        maker._add_half_month(half_event, uposatha_event)

        season = maker._next_season

        self.assertEqual("Hemanta", season.season_name)
        self.assertEqual(8, season.uposatha_count)
        self.assertEqual(2, len(season.events))
        self.assertEqual("Waning", season.events[0].moon_name)
        self.assertEqual("New", season.events[1].moon_name)

    def test_season_has_changed(self):
        first_uposatha_detail = {"date": date(2010, 12, 6), "summary": "New Moon - 15 day Hemanta 1/8"}

        events = details_to_events([first_uposatha_detail])

        self.assertEqual(1, len(events))

        first_uposatha_event = events[0]

        maker = SeasonMaker([])
        maker._next_season.season_name = "Vassāna"
        result = maker._season_has_changed(first_uposatha_event)

        self.assertTrue(result)

    def test_season_not_initialised(self):
        # For the very first event, we have a new Season without
        # any content.
        detail = {"date": date(2010, 12, 6), "summary": "New Moon - 15 day Hemanta 1/8"}
        event = details_to_events([detail])[0]
        maker = SeasonMaker([])
        self.assertFalse(maker._season_has_changed(event))


    def test_two_pairs_same_season(self):
        details = [
            {"date": date(2010, 11, 29), "summary": "Waning Moon"},
            {"date": date(2010, 12, 6), "summary": "New Moon - 15 day Hemanta 1/8"},
            {"date": date(2010, 12, 14), "summary": "Waxing Moon"},
            {"date": date(2010, 12, 21), "summary": "Full Moon - 15 day Hemanta 2/8"}
        ]

        two_pairs_of_events = details_to_events(details)
        self.assertEqual(4, len(two_pairs_of_events))

        maker = SeasonMaker(two_pairs_of_events)
        seasons = maker.get_seasons()

        self.assertEqual(1, len(seasons))
        self.assertEqual("Hemanta", seasons[0].season_name)


    def test_two_pairs_different_season(self):
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

        self.assertEqual(2, len(seasons))

        self.assertEqual("Hemanta", seasons[0].season_name)
        self.assertEqual("Gimha", seasons[1].season_name)


class TestEvent(TestCase):
    def test_set_moon_phase(self):
        waxing_detail = {"date": date(2022, 3, 18), "summary": "Waxing Moon"}
        event = Event(waxing_detail)
        event._set_moon_phase()
        self.assertEqual("Waxing", event.moon_name)

        waning_detail = {"date": date(2022, 3, 18), "summary": "Waning Moon"}
        event = Event(waning_detail)
        event._set_moon_phase()
        self.assertEqual("Waning", event.moon_name)

        full_detail = {"date": date(2022, 3, 18), "summary": "Full Moon - 15 day Hemanta 6/8"}
        event = Event(full_detail)
        event._set_moon_phase()
        self.assertEqual("Full", event.moon_name)

        new_detail = {"date": date(2022, 3, 18), "summary": "New Moon - 15 day Hemanta 5/8"}
        event = Event(new_detail)
        event._set_moon_phase()
        self.assertEqual("New", event.moon_name)

        vassa_first_day_detail = {"date": date(2022, 3, 18), "summary": "First day of Vassa"}
        event = Event(vassa_first_day_detail)
        event._set_moon_phase()
        self.assertEqual("None", event.moon_name)

    def test_set_special_day(self):
        # Every special day falls on a full moon day.
        full_detail = {"date": date(2022, 3, 18), "summary": "Full Moon - 15 day Hemanta 6/8"}
        special_detail = {"date": date(2022, 3, 18), "summary": "Āsāḷha Pūjā"}
        event = Event(full_detail)
        event.add_details(special_detail)
        event._set_moon_phase()
        event._set_special_days()
        self.assertEqual("Āsāḷha Pūjā", event.special_day)

    def test_set_first_vassa(self):
        # The first day of vassa is not a moon day.
        detail = {"date": date(2022, 3, 18), "summary": "First day of Vassa"}
        event = Event(detail)
        event._set_vassa_days()
        self.assertEqual("First day of Vassa", event.vassa_day)

    def test_set_last_vassa_day(self):
        # The only day with three summaries is the end of the rains.
        full_detail = {"date": date(2022, 3, 18), "summary": "Full Moon - 15 day Hemanta 6/8"}
        special_detail = {"date": date(2022, 3, 18), "summary": "Pavāraṇā Day"}
        last_detail = {"date": date(2022, 3, 18), "summary": "Last day of Vassa"}

        event = Event(full_detail)
        event.add_details(special_detail)
        event.add_details(last_detail)

        event._set_vassa_days()
        self.assertEqual("Last day of Vassa", event.vassa_day)

    def test_complete(self):
        full_detail = {"date": date(2022, 3, 18), "summary": "Full Moon - 15 day Hemanta 6/8"}
        special_detail = {"date": date(2022, 3, 18), "summary": "Pavāraṇā Day"}
        last_detail = {"date": date(2022, 3, 18), "summary": "Last day of Vassa"}

        event = Event(full_detail)
        event.add_details(special_detail)
        event.add_details(last_detail)

        event.complete()

        self.assertEqual("Full", event.moon_name)
        self.assertEqual("Pavāraṇā Day", event.special_day)
        self.assertEqual("Last day of Vassa", event.vassa_day)

    def test_set_extended_summary(self):
        full_detail = {"date": date(2022, 3, 18), "summary": "Full Moon - 15 day Hemanta 6/8"}

        event = Event(full_detail)
        event.complete()

        season = event._extended_summary.season_name()
        self.assertEqual("Hemanta", season)

    def test_is_uposatha(self):
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

        self.assertFalse(waxing_event.is_uposatha())
        self.assertFalse(waning_event.is_uposatha())

        self.assertTrue(full_event.is_uposatha())
        self.assertTrue(new_event.is_uposatha())

    def test_is_end_of_season(self):
        half_moon_detail = {"date": date(2010, 7, 19), "summary": "Waxing Moon"}
        uposatha_end_detail = {"date": date(2010, 7, 26), "summary": "Full Moon - 15 day Gimha 10/10"}
        uposatha_not_end_detail = {"date": date(2010, 8, 10), "summary": "New Moon - 15 day Vassāna 1/8"}

        half_moon_event = Event(half_moon_detail)
        uposatha_end_event = Event(uposatha_end_detail)
        uposatha_not_end_event = Event(uposatha_not_end_detail)

        half_moon_event.complete()
        uposatha_end_event.complete()
        uposatha_not_end_event.complete()

        self.assertFalse(half_moon_event.is_end_of_season())
        self.assertFalse(uposatha_not_end_event.is_end_of_season())
        self.assertTrue(uposatha_end_event.is_end_of_season())


class TestExtendedSummary(TestCase):
    def setUp(self):
        self.full = ExtendedSummary("Full Moon - 15 day Hemanta 6/8")
        self.new = ExtendedSummary("New Moon - 14 day Gimha 3/10")

    def test_days_in_fortnight(self):
        self.assertEqual(15, self.full.uposatha_days())
        self.assertEqual(14, self.new.uposatha_days())
        # TODO: Check exceptions

    def test_season_name(self):
        self.assertEqual("Hemanta", self.full.season_name())
        self.assertEqual("Gimha", self.new.season_name())

    def test_uposatha_number(self):
        self.assertEqual(6, self.full.uposatha_of_season())
        self.assertEqual(3, self.new.uposatha_of_season())

    def test_uposatha_in_season(self):
        self.assertEqual(8, self.full.uposathas_in_season())
        self.assertEqual(10, self.new.uposathas_in_season())

class TestSeason(TestCase):
    def test_end_date(self):
        details = [
            {"date": date(2010, 11, 29), "summary": "Waning Moon"},
            {"date": date(2010, 12, 6), "summary": "New Moon - 15 day Hemanta 1/8"},
            {"date": date(2010, 12, 14), "summary": "Waxing Moon"},
            {"date": date(2010, 12, 21), "summary": "Full Moon - 15 day Hemanta 2/8"}
        ]

        season = details_to_seasons(details)[0]
        self.assertEqual(date(2010, 12, 21), season.end_date())

    def test_english_name(self):
        season = Season()
        season.season_name = "Hemanta"
        self.assertEqual("Cold", season.english_name())
        season.season_name = "Gimha"
        self.assertEqual("Hot", season.english_name())
        season.season_name = "Vassāna"
        self.assertEqual("Rainy", season.english_name())
