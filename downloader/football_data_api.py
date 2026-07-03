"""
football_data_api.py

Downloads historical match data from football-data.co.uk straight into the
Bronze landing folder (data/bronze/) - no separate "raw" copy step. That
separation only existed because Databricks Unity Catalog Volumes couldn't
be written into directly without extra ceremony; developing locally, Bronze
just IS the landing zone.

Usage as a library:
    from downloader.football_data_api import download_main_leagues, download_extra_leagues
    download_main_leagues(countries=["england"], seasons=[("2526", "2025-26")])

Usage as a script (does the full pull - all main + extra leagues):
    python downloader/football_data_api.py

Resumable by design: download_file skips anything already on disk and
non-empty, so a dropped connection just means re-running picks up where
it left off instead of starting over.
"""

import os
import time

import requests

BASE_URL = "https://www.football-data.co.uk"
OUTPUT_DIR = os.path.join("data", "bronze")

# Division names match what used to be scripts/rename_league_folders.py -
# written out in full here directly, so there's no separate renaming step.
MAIN_LEAGUES = {
    "england": {"name": "England", "divisions": {
        "E0": "Premier League", "E1": "Championship",
        "E2": "League One", "E3": "League Two", "EC": "National League"}},
    "scotland": {"name": "Scotland", "divisions": {
        "SC0": "Scottish Premiership", "SC1": "Scottish Championship",
        "SC2": "Scottish League One", "SC3": "Scottish League Two"}},
    "germany": {"name": "Germany", "divisions": {
        "D1": "Bundesliga", "D2": "2. Bundesliga"}},
    "italy": {"name": "Italy", "divisions": {
        "I1": "Serie A", "I2": "Serie B"}},
    "spain": {"name": "Spain", "divisions": {
        "SP1": "La Liga", "SP2": "La Liga 2"}},
    "france": {"name": "France", "divisions": {
        "F1": "Ligue 1", "F2": "Ligue 2"}},
    "netherlands": {"name": "Netherlands", "divisions": {"N1": "Eredivisie"}},
    "belgium": {"name": "Belgium", "divisions": {"B1": "Belgian Pro League"}},
    "portugal": {"name": "Portugal", "divisions": {"P1": "Primeira Liga"}},
    "turkey": {"name": "Turkey", "divisions": {"T1": "Super Lig"}},
    "greece": {"name": "Greece", "divisions": {"G1": "Super League Greece"}},
}

# (url_code, display_label) — "/" can't be used in filenames, so folders
# use "2025-26" rather than "2025/26"
MAIN_SEASONS = [
    ("2526", "2025-26"), ("2425", "2024-25"), ("2324", "2023-24"),
    ("2223", "2022-23"), ("2122", "2021-22"), ("2021", "2020-21"),
    ("1920", "2019-20"), ("1819", "2018-19"), ("1718", "2017-18"),
    ("1617", "2016-17"), ("1516", "2015-16"), ("1415", "2014-15"),
    ("1314", "2013-14"), ("1213", "2012-13"), ("1112", "2011-12"),
    ("1011", "2010-11"), ("0910", "2009-10"), ("0809", "2008-09"),
    ("0708", "2007-08"), ("0607", "2006-07"), ("0506", "2005-06"),
]

EXTRA_LEAGUES = {
    "argentina": ("ARG", "Primera Division"), "austria": ("AUT", "Bundesliga"),
    "brazil": ("BRA", "Serie A"), "china": ("CHN", "Super League"),
    "denmark": ("DNK", "Superliga"), "finland": ("FIN", "Veikkausliiga"),
    "ireland": ("IRL", "Premier Division"), "japan": ("JPN", "J-League"),
    "mexico": ("MEX", "Liga MX"), "norway": ("NOR", "Eliteserien"),
    "poland": ("POL", "Ekstraklasa"), "romania": ("ROU", "Liga 1"),
    "russia": ("RUS", "Premier League"), "sweden": ("SWE", "Allsvenskan"),
    "switzerland": ("SWZ", "Super League"), "usa": ("USA", "MLS"),
}


def download_file(url: str, dest_path: str, skip_existing: bool = True) -> str:
    """Returns one of: "skipped", "ok", "miss", "error" """
    if skip_existing and os.path.exists(dest_path) and os.path.getsize(dest_path) > 0:
        return "skipped"
    try:
        resp = requests.get(url, timeout=20)
        if resp.status_code == 200 and len(resp.content) > 0:
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            with open(dest_path, "wb") as f:
                f.write(resp.content)
            return "ok"
        return "miss"
    except requests.RequestException:
        return "error"


def download_main_leagues(seasons=None, countries=None, skip_existing=True):
    seasons = seasons or MAIN_SEASONS
    countries = countries or list(MAIN_LEAGUES.keys())
    counts = {"ok": 0, "skipped": 0, "miss": 0, "error": 0}

    for country_key in countries:
        country = MAIN_LEAGUES[country_key]
        print(f"\n{country['name']}")
        for div_code, div_name in country["divisions"].items():
            for url_code, label in seasons:
                url = f"{BASE_URL}/mmz4281/{url_code}/{div_code}.csv"
                dest = os.path.join(OUTPUT_DIR, "main_leagues", country_key, div_name, f"{label}.csv")
                result = download_file(url, dest, skip_existing)
                counts[result] += 1
                tag = {"ok": "OK   ", "skipped": "SKIP ", "miss": "MISS ", "error": "ERROR"}[result]
                print(f"  {tag} {div_name} ({div_code}) — {label}")
                if result == "ok":
                    time.sleep(0.3)

    print(f"\nDone: {counts['ok']} downloaded, {counts['skipped']} already had, "
          f"{counts['miss']} missing, {counts['error']} errors")
    return counts


def download_extra_leagues(countries=None, skip_existing=True):
    countries = countries or list(EXTRA_LEAGUES.keys())
    counts = {"ok": 0, "skipped": 0, "miss": 0, "error": 0}

    print("Extra Leagues")
    for country_key in countries:
        code_, league_name = EXTRA_LEAGUES[country_key]
        url = f"{BASE_URL}/new/{code_}.csv"
        dest = os.path.join(OUTPUT_DIR, "extra_leagues", f"{code_}.csv")
        result = download_file(url, dest, skip_existing)
        counts[result] += 1
        tag = {"ok": "OK   ", "skipped": "SKIP ", "miss": "MISS ", "error": "ERROR"}[result]
        print(f"  {tag} {country_key.title()} — {league_name} ({code_})")
        if result == "ok":
            time.sleep(0.3)

    print(f"\nDone: {counts['ok']} downloaded, {counts['skipped']} already had, "
          f"{counts['miss']} missing, {counts['error']} errors")
    return counts


if __name__ == "__main__":
    download_main_leagues()
    download_extra_leagues()
