from unittest import TestCase
from datetime import date

from forest_sangha_moons import MahanikayaCalendar, Event, ExtendedSummary

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

    def test_week_number(self):
        self.assertEqual(6, self.full.week_of_season())
        self.assertEqual(3, self.new.week_of_season())

    def test_weeks_in_season(self):
        self.assertEqual(8, self.full.weeks_in_season())
        self.assertEqual(10, self.new.weeks_in_season())