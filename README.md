# Football Data Warehouse

End-to-end football analytics pipeline covering 20 years (2005–2026) of match
data across 11 countries, built on Databricks using medallion architecture
(Bronze / Silver / Gold).

## Why this project

Started as a scoped-down restart after an earlier attempt at a South African
crime statistics pipeline turned out to be too much, too soon — messy
government data, no API, inconsistent file structures across years. This
project deliberately picks a cleaner data source (football-data.co.uk, plain
CSV, no auth, no rate limits) so the focus stays on learning Databricks and
the medallion pattern properly, not fighting the data source itself.

That said, at this scale (hundreds of thousands of rows) there IS a real
data engineering problem worth solving: **schema drift**. Column structure
is not consistent across 20 years of files — older seasons have fewer
betting-odds columns, smaller leagues track fewer match stats. Reconciling
that honestly (not just papering over it) is the actual technical substance
of this project.

## Architecture

```
Raw CSVs (data/raw/, organized by country/division/season)
        ↓
Bronze — frozen file copy only (Volume, no tables - see below)
        ↓
Silver — one table per league, seasons unioned + schema drift handled
        ↓
Gold — star schema: fact_matches + dim_teams / dim_leagues / dim_seasons
        ↓
EDA (SQL)  →  Model (match outcome classifier)
```

Bronze is deliberately file-only (no Delta tables) rather than the more
typical one-table-per-source design: the original per-league-per-season
Bronze design hit ~470 tables and triggered a Unity Catalog 500-table
metastore quota warning before Silver or Gold even existed. See
[docs/schema_notes.md](docs/schema_notes.md) for the full writeup.

Catalog layout:
```
workspace (catalog)
├── default   → Volume: football_raw       (original downloaded CSVs)
├── bronze    → Volume: football_bronze     (frozen file copy, no tables)
├── silver    → one Delta table per league  (england_premier_league, ...)
└── gold      → star schema tables (not built yet)
```

## Data source

- **Main leagues** (England, Scotland, Germany, Italy, Spain, France,
  Netherlands, Belgium, Portugal, Turkey, Greece): one CSV per season per
  division, `football-data.co.uk/mmz4281/{season}/{division}.csv`
- **Extra leagues** (Argentina, Brazil, Japan, USA/MLS, and 12 others):
  one all-seasons-in-one CSV per league,
  `football-data.co.uk/new/{code}.csv`

See [docs/data_sources.md](docs/data_sources.md) for the full breakdown and
licensing note.

## Tech stack

- Databricks Free Edition (serverless compute, Delta Lake, MLflow, SQL)
- Python / pandas / PySpark
- Databricks Repos (this repo, Git-synced)

## Status

🚧 Data collection complete (478 files: 462 main-league + 16 extra-league).
Bronze redesigned to a plain file copy (see Architecture above). Silver:
all 5 England divisions done (Premier League, Championship, League One,
League Two, National League) as individual tables in `workspace.silver`.
Next: Scotland, then the remaining 9 main-league countries and 16 extra
leagues, one Silver table per league.

## Author

Morobang Tshigidimisa ([@Morobang](https://github.com/Morobang))
