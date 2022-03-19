from unittest import TestCase
from datetime import date

from forest_sangha_moons.MahanikayaCalendar import Event

class TestEvent(TestCase):
    def test_set_moon_phase(self):
        # Create an event
        detail_one = {"date": date(2022, 3, 18), "summary": "Waxing Moon"}
        event = Event(detail_one)
        event._set_moon_phase()

        self.assertEqual("Waxing", event.moon_phase)