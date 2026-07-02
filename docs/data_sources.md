# Data Sources

## football-data.co.uk

Source: Joseph Buchdahl's football-data.co.uk, publishing football results,
stats, and betting odds in CSV format since 2001.

**License note:** data is provided for personal/research use. If sharing
derived datasets or analysis publicly, credit the source
(football-data.co.uk).

### Main leagues — season-by-season files

One CSV per season per division. URL pattern:
```
https://www.football-data.co.uk/mmz4281/{season_code}/{division_code}.csv
```
`season_code` example: `2526` = 2025/26 season.

| Country | Divisions |
|---|---|
| England | E0 (Premier League), E1 (Championship), E2 (League 1), E3 (League 2), EC (Conference) |
| Scotland | SC0 (Premiership), SC1, SC2, SC3 |
| Germany | D1 (Bundesliga), D2 (Bundesliga 2) |
| Italy | I1 (Serie A), I2 (Serie B) |
| Spain | SP1 (La Liga Primera), SP2 (Segunda) |
| France | F1 (Le Championnat), F2 (Division 2) |
| Netherlands | N1 (Eredivisie) |
| Belgium | B1 (Jupiler League) |
| Portugal | P1 (Liga I) |
| Turkey | T1 (Ligi 1) |
| Greece | G1 (Ethniki Katigoria) |

Seasons collected: 2005-06 through 2025-26 (20 seasons).

### Extra leagues — all-seasons-in-one files

One CSV per league, covering every available season at once. URL pattern:
```
https://www.football-data.co.uk/new/{code}.csv
```

Countries: Argentina, Austria, Brazil, China, Denmark, Finland, Ireland,
Japan, Mexico, Norway, Poland, Romania, Russia, Sweden, Switzerland, USA.

### Known data quality issues (found during collection / to verify in Silver)

- **Schema drift**: column count and betting-odds coverage varies
  significantly between older (2005-06) and recent (2025-26) seasons, and
  between top divisions and lower/smaller-league divisions
- **Encoding**: source files are Windows-1252, not UTF-8 — must specify
  `encoding='cp1252'` when reading, or accented team/player names will
  break
- **Team name consistency**: not yet verified whether the same club is
  spelled identically across different seasons/files (e.g. "Man United"
  vs "Manchester United") — to be checked in Silver

## Download method

Collected via a custom Python notebook
(`downloader/football_data_downloader.ipynb`) rather than the site's own
bulk-zip downloads, to get consistent per-file organization by
country/division/season and to make the process resumable (skips
already-downloaded files, safe to re-run after a network interruption).
