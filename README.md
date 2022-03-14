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

There's no API at this point as I'm working on the importing first.