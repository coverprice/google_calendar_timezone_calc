**What:** This tool helps solve a problem with Google Calendar: it has terrible timezone selection.
Given a city name, this tool prints out the equivalent Google Calendar timezone for that city.

**Why:** For example, if you're adding an event for a flight and want
to specify departure/arrival in different timezones, you must pick from a list of GMT offsets paired with some
random cities. If you don't know the timezone of your target city, it's hard to know which one to pick.

**How:** `google_calendar_timezone_calc.py SOME_CITY_NAME`

If you enter an ambiguous name (e.g. "London") then it will present a list of options to disambiguate it.
