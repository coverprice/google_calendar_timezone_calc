#!/usr/bin/env python
# Google Calendar has terrible timezone selection. For example: If you're adding an event for a flight and want
# to specify the start/end timezones, it gives you a list of GMT offsets paired with some random cities, so if you
# don't know the timezone of your target city, it's hard to know which one to pick.
#
# This tool takes a city name and spits out the Google Calendar timezone for that city. If you enter a city name
# that's ambiguous (e.g. "London") then it will present a list of options to disambiguate it.

from pathlib import Path
from argparse import ArgumentParser
import json
import re


def get_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Converts a city + time into a GMT offset suitable for use in Google Calendar")
    parser.add_argument('city', type=str, help="City name")
    return parser


def find_city(target_city: str) -> list[dict]:
    with Path(__file__).parent.joinpath('node_modules/city-timezones/data/cityMap.json').open(mode='r') as fh:
        """
        Example entry:
          {
            "city": "Chicago",
            "city_ascii": "Chicago",
            "lat": 41.82999066,
            "lng": -87.75005497,
            "pop": 5915976,
            "country": "United States of America",
            "iso2": "US",
            "iso3": "USA",
            "province": "Illinois",
            "exactCity": "Chicago",
            "exactProvince": "IL",
            "state_ansi": "IL",
            "timezone": "America/Chicago"
          }
        """
        city_map = json.load(fh)
    target_city = target_city.lower()
    return list(filter(lambda x: x['city_ascii'].lower().startswith(target_city), city_map))


def parse_city(target_city: str) -> str:
    matches = find_city(target_city)
    if len(matches) == 0:
        sys.exit(f"No city found by the name: '{target_city}'")
    elif len(matches) == 1:
        return matches[0]

    out_rows = [
        ["IDX", "CITY", "PROVINCE", "COUNTRY", "TIMEZONE"],
    ]
    for idx, city_rec in enumerate(matches, start=1):
        out_rows.append(
            [str(idx), city_rec['city_ascii'], city_rec.get('province', ""), city_rec['country'], city_rec['timezone']]
        )
    max_widths = [0] * len(out_rows[0])
    for i in out_rows:
        for j, item in enumerate(i):
            max_widths[j] = max(max_widths[j], len(item))

    print("==== Multiple matches found, please select a city ====")
    for i in out_rows:
        for j, item in enumerate(i):
            print(f"{item:{max_widths[j]}}  ", end="")
        print()

    while True:
        selection = input("Select a city's index number: ").strip()
        if not re.match('^[0-9]+$', selection):
            continue
        idx = int(selection)
        if idx < 1 or idx > len(matches):
            continue
        return matches[idx]


def main():
    args = get_parser().parse_args()
    target_city: dict = parse_city(args.city)

    with Path(__file__).parent.joinpath('node_modules/google-timezones-json/timezones.json').open(mode='r') as fh:
        timezone_to_gcal_timezone = json.load(fh)

    gcal_timezone = timezone_to_gcal_timezone[target_city['timezone']]
    print(gcal_timezone)


main()
