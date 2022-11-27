# My minimum viable product.
import pathlib
import icalendar
from forest_sangha_moons.MahanikayaCalendar import MahanikayaCalendar

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", dest="myFile", help="Open specified file")
args = parser.parse_args()
myFile = args.myFile

with open(myFile, "r") as f:
    content = f.read()

ical = icalendar.Calendar.from_ical(content)
calendar = MahanikayaCalendar()
calendar.import_ical(ical)

if calendar.today_is_uposatha():
    print("Today is the uposatha")

print("Days until next uposatha: {}".format(
    calendar.days_to_next_uposatha()
))

next_uposatha = calendar.next_uposatha()

print("The next uposatha is a {} day {} moon on {}".format(
    next_uposatha.uposatha_days,
    next_uposatha.moon_name,
    next_uposatha.date.strftime("%A, %d %b %y")
))

print("It is uposatha {} of {} of the {} season".format(
    next_uposatha.uposatha_of_season,
    next_uposatha.season.uposatha_count,
    next_uposatha.season.season_name
))

special = next_uposatha.special_day

if special:
    print("It is: {}".format(special))

