from datetime import date
from forest_sangha_moons.MahanikayaCalendar import Event

def uposatha_lengths():
    lengths = []
    for number in range(1, 9):
        if number == 3 or number == 7:
            lengths.append(14)
        else:
            lengths.append(15)

    return lengths

def generate_event():
    details = {"date": date(2022, 12, 29), "summary": ""}
    event = Event(details)
    return event