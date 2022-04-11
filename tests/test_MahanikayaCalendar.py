from unittest import TestCase
from datetime import date

from forest_sangha_moons import MahanikayaCalendar, Event
from forest_sangha_moons.MahanikayaCalendar import ExtendedSummary, SeasonMaker

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

class TestSeasonMaker(TestCase):
    def details_to_seasons(self, details):
        cal = MahanikayaCalendar()
        for moon in details:
            cal._process_details(moon)
        maker = SeasonMaker(cal.events)
        return maker.get_seasons()

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

    def test_seasons_first_lunar_cycle(self):
        # These are the first four VEVENTS from the real data.
        lunar_cycle = [
            {"date": date(2010, 1, 8), "summary": "Waning Moon"},
            {"date": date(2010, 1, 15), "summary": "New Moon - 15 day Hemanta 5/8"},
            {"date": date(2010, 1, 23), "summary": "Waxing Moon"},
            {"date": date(2010, 1, 30), "summary": "Full Moon - 15 day Hemanta 6/8"}
        ]

        seasons = self.details_to_seasons(lunar_cycle)

        self.assertEqual(1, len(seasons), "There should be exactly one season")

        season = season[0]

        self.assertEqual("Hemanta", season.season_name)
        self.assertEqual(8, season.uposatha_count)
        self.assertEqual(4, len(season.events))

        event = events[0]

        self.assertEqual("Waxing", event.moon_name)
        self.assertEqual("Hemanta", event.season.season_name)

    def test_season_change(self):
        season_change = [
            # End of cold season
            {"date": date(2010, 2, 28), "summary": "Full Moon - 15 day Hemanta 8/8"},
            {"date": date(2022, 2, 28), "summary": "Māgha Pūjā"},
            # Changing to hot season
            {"date": date(2010, 3, 8), "summary": "Waning Moon"},
            {"date": date(2010, 3, 15), "summary": "New Moon - 15 day Gimha 1/10"},
        ]

        seasons = self.details_to_seasons(season_change)

        self.assertEqual(2, len(seasons), "There should be two seasons")

        self.assertEqual("Hemanta", seasons[0].season_name, "First season is Hemanta")
        self.assertEqual("Gimha", seasons[1].season_name, "Second season is Gimha")

        self.assertEqual(2, len(seasons[0].events), "First season has two events")
        self.assertEqual(2, len(seasons[1].events), "Second seasons has two events")


    def test_trailing_waning_moon(self):
        trailing_waning = [
            # End of cold season
            {"date": date(2010, 2, 28), "summary": "Full Moon - 15 day Hemanta 8/8"},
            {"date": date(2022, 2, 28), "summary": "Māgha Pūjā"},
            # A new hot season, but only a waning moon without an
            # extended summary and no subsequent new moon.
            {"date": date(2010, 3, 8), "summary": "Waning Moon"}
        ]

        seasons = self.details_to_seasons(trailing_waning)

        self.assertEqual(2, len(seasons), "There should be two seasons")

        self.assertEqual("Hemanta", seasons[0].season_name, "First season is Hemanta")
        self.assertEqual("Gimha", seasons[1].season_name, "Second season is Gimha")

        self.assertEqual(2, len(seasons[0].events), "First season has two events")
        self.assertEqual(1, len(seasons[1].events), "Second seasons has one event")


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

    def test_uposatha_number(self):
        self.assertEqual(6, self.full.uposatha_of_season())
        self.assertEqual(3, self.new.uposatha_of_season())

    def test_uposatha_in_season(self):
        self.assertEqual(8, self.full.uposathas_in_season())
        self.assertEqual(10, self.new.uposathas_in_season())
