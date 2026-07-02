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
Bronze — ingested as-is, tagged with source metadata from folder path
        ↓
Silver — schema drift reconciled, standardized columns, clean team names
        ↓
Gold — star schema: fact_matches + dim_teams / dim_leagues / dim_seasons
        ↓
EDA (SQL)  →  Model (match outcome classifier)
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

🚧 Data collection complete (451 files, main + extra leagues). Bronze
ingestion in progress, currently scoped to England only before expanding
to all 11 countries.

## Author

Morobang Tshigidimisa ([@Morobang](https://github.com/Morobang))
