from unittest import TestCase
from datetime import date

from forest_sangha_moons.MahanikayaCalendar import MahanikayaCalendar, Event, ExtendedSummary

class TestMahaNikayaCalendar(TestCase):
    def test_event_with_one_detail(self):
        waxing_detail = {"date": date(2022, 3, 18), "summary": "Waxing Moon"}

        cal = MahanikayaCalendar()
        cal._process_details(waxing_detail)

        self.assertEqual(1, len(cal.events))
        self.assertEqual("Waxing", cal.events[0].moon_name)

    def test_two_events_with_one_detail_each(self):
        waxing_detail = {"date": date(2022, 3, 18), "summary": "Waxing Moon"}
        full_detail = {"date": date(2022, 3, 19), "summary": "Full Moon - 15 day Hemanta 6/8"}

        cal = MahanikayaCalendar()
        cal._process_details(waxing_detail)
        cal._process_details(full_detail)

        self.assertEqual("Waxing", cal.events[0].moon_name)
        self.assertEqual("Full", cal.events[1].moon_name)

    def test_add_first_event(self):
        waxing_detail = {"date": date(2022, 3, 18), "summary": "Waxing Moon"}

        cal = MahanikayaCalendar()
        cal._add_first_event(waxing_detail)

        self.assertEqual(1, len(cal.events))
        self.assertEqual("Waxing", cal.events[0].moon_name)


    def test_add_subsequent_event(self):
        waxing_detail = {"date": date(2022, 3, 18), "summary": "Waxing Moon"}
        full_detail = {"date": date(2022, 3, 19), "summary": "Full Moon - 15 day Hemanta 6/8"}

        cal = MahanikayaCalendar()
        cal._add_first_event(waxing_detail)
        cal._add_subsequent_event(full_detail)

        self.assertEqual(2, len(cal.events))
        self.assertEqual("Waxing", cal.events[0].moon_name)
        self.assertEqual("Full", cal.events[1].moon_name)

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

    def test_process(self):
        full_detail = {"date": date(2022, 3, 18), "summary": "Full Moon - 15 day Hemanta 6/8"}
        special_detail = {"date": date(2022, 3, 18), "summary": "Pavāraṇā Day"}
        last_detail = {"date": date(2022, 3, 18), "summary": "Last day of Vassa"}

        event = Event(full_detail)
        event.add_details(special_detail)
        event.add_details(last_detail)

        event.process()

        self.assertEqual("Full", event.moon_name)
        self.assertEqual("Pavāraṇā Day", event.special_day)
        self.assertEqual("Last day of Vassa", event.vassa_day)

    def test_set_extended_summary(self):
        full_detail = {"date": date(2022, 3, 18), "summary": "Full Moon - 15 day Hemanta 6/8"}

        event = Event(full_detail)
        event.process()

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