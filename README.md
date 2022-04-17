# uposatha-ical

Like a lot of monks, I rely on the [Forest Sangha Calendars](https://forestsangha.org/community/calendars/year_planners/2022)
The data for this calendar exists in [icalendar form](https://en.wikipedia.org/wiki/ICalendar) and
this package will provide a python interface to the information within. This could then be used
for notifications or an IoT project.

## Analysis

The starting point for this project is an ical file: 

http://splendidmoons.github.io/ical/mahanikaya.ical

This was created in 2016 and contains Maha Nikaya lunar calendar events from 2010 to 2030. I 
downloaded the file and extracted `DTSTART` and `SUMMARY` properties of each`VEVENT`component,
discarding any components that did not have both. Exporting the pairs to a CSV file and 
exploring the data-set in RStudio I make the following assertions:

- Events are in date order.
- There are 4 moon days: Full, New, Waxing, Waning.
- All events fall on a moon day except "First Day of Vassa".
- Waxing moon, waning moon, new moon and first day of vassa always occur alone.
- Full moon days can occur alone.
- Full moon days can be concurrent with a "special day" `VEVENT` summary such as Māgha Pūjā.
- The Pavāraṇā Day has three `VEVENT`s associated with it:
  - A full moon.
  - Pavāraṇā Day.
  - Last day of Vassa.
- No other day has 3 `VEVENTS`

I use these assumptions when processing the ical file so things may break if the file format
changes.

## API

### Import the Forest Sangha calendar

```python
import icalendar
from forest_sangha_moons import MahanikayaCalendar

with open("mahanikaya.ical", "r") as f:
    content = f.read()

ical = icalendar.Calendar.from_ical(content)
calendar = MahanikayaCalendar()
calendar.import_ical(ical)
```

### Use calendar functions

```python
robe_up = calendar.today_is_uposatha()
days_left = calendar.days_to_next_uposatha()
next_uposatha = calendar.next_uposatha()
```

### Get details of events

```python
print("The next uposatha is a {} day {} moon on {}".format(
    next_uposatha.uposatha_days,
    next_uposatha.moon_name,
    next_uposatha.date.strftime("%d %b %y")
))
```

### Get season details

```python
print("It is uposatha {} of {} of the {} season".format(
    next_uposatha.uposatha_of_season,
    next_uposatha.season.uposatha_count,
    next_uposatha.season.season_name
))
```