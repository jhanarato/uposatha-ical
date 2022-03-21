from unittest import TestCase
from datetime import date

from forest_sangha_moons.MahanikayaCalendar import Event

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
        event.update(special_detail)
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
        event.update(special_detail)
        event.update(last_detail)

        event._set_vassa_days()
        self.assertEqual("Last day of Vassa", event.vassa_day)

    def test_process(self):
        full_detail = {"date": date(2022, 3, 18), "summary": "Full Moon - 15 day Hemanta 6/8"}
        special_detail = {"date": date(2022, 3, 18), "summary": "Pavāraṇā Day"}
        last_detail = {"date": date(2022, 3, 18), "summary": "Last day of Vassa"}

        event = Event(full_detail)
        event.update(special_detail)
        event.update(last_detail)

        event.process()

        self.assertEqual("Full", event.moon_name)
        self.assertEqual("Pavāraṇā Day", event.special_day)
        self.assertEqual("Last day of Vassa", event.vassa_day)