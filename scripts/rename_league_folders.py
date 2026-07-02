"""
rename_league_folders.py

Renames existing division-code folders (E0, D1, SP1, ...) to their proper
league names (Premier League, Bundesliga, La Liga, ...), so the folder
structure reads naturally instead of requiring you to memorize codes.

The original code is NOT lost — it's still embedded in every row once
Bronze ingestion runs (extracted from the file path at ingest time), and
this same CODE_TO_NAME mapping is what Bronze will use to look it up.

Run this once, from the repo root:
    python scripts/rename_league_folders.py
"""

import os

CODE_TO_NAME = {
    "E0": "Premier League",
    "E1": "Championship",
    "E2": "League One",
    "E3": "League Two",
    "EC": "National League",
    "SC0": "Scottish Premiership",
    "SC1": "Scottish Championship",
    "SC2": "Scottish League One",
    "SC3": "Scottish League Two",
    "D1": "Bundesliga",
    "D2": "2. Bundesliga",
    "I1": "Serie A",
    "I2": "Serie B",
    "SP1": "La Liga",
    "SP2": "La Liga 2",
    "F1": "Ligue 1",
    "F2": "Ligue 2",
    "N1": "Eredivisie",
    "B1": "Belgian Pro League",
    "P1": "Primeira Liga",
    "T1": "Super Lig",
    "G1": "Super League Greece",
}

MAIN_LEAGUES_DIR = os.path.join("data", "raw", "main_leagues")


def rename_division_folders():
    if not os.path.isdir(MAIN_LEAGUES_DIR):
        print(f"Can't find {MAIN_LEAGUES_DIR} — run this from the repo root.")
        return

    renamed, skipped = 0, 0

    for country in sorted(os.listdir(MAIN_LEAGUES_DIR)):
        country_path = os.path.join(MAIN_LEAGUES_DIR, country)
        if not os.path.isdir(country_path):
            continue

        for division_folder in sorted(os.listdir(country_path)):
            old_path = os.path.join(country_path, division_folder)
            if not os.path.isdir(old_path):
                continue

            if division_folder in CODE_TO_NAME:
                new_name = CODE_TO_NAME[division_folder]
                new_path = os.path.join(country_path, new_name)
                if os.path.exists(new_path):
                    print(f"  SKIP  {old_path} — target already exists")
                    skipped += 1
                    continue
                os.rename(old_path, new_path)
                print(f"  OK    {country}/{division_folder} -> {country}/{new_name}")
                renamed += 1
            else:
                print(f"  ????  {old_path} — no mapping found, left as-is")
                skipped += 1

    print(f"\nDone: {renamed} renamed, {skipped} skipped")


if __name__ == "__main__":
    rename_division_folders()
