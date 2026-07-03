# Schema Notes

Living log of schema drift and data quality issues found while building the
pipeline. Update this as new issues are discovered — this is the actual
evidence of the engineering work done on this project, not just the code.

## Format

```
### [Layer] Issue found on [date]
**What:** description of the problem
**Where:** which files/seasons/leagues affected
**Decision:** how it was handled and why
```

---

### [Bronze] Column count mismatch, older vs recent seasons
**What:** 2005-06 season files have far fewer betting-odds columns than
2025-26 files (bookmakers have added markets over time).
**Where:** All main leagues, most visible in England E0.
**Decision:** TBD — likely keep only the core columns present across all
seasons in Silver, rather than trying to backfill missing odds columns for
older data.

### [Bronze] Ragged rows mid-file (not just header ghost columns)
**What:** A handful of 2007-08 season files (France Ligue 2, Netherlands
Eredivisie, Portugal Primeira Liga, +2 more) have a normal-width header but
rows partway through the file carry 3 extra empty trailing cells — pandas'
C parser raises "Error tokenizing data" on the ragged width and refuses to
read the file at all. Different bug from the header-only ghost-column case
(where the header itself has trailing commas and pandas just auto-names
`Unnamed: N` columns).
**Where:** 5 of 462 main-league files, all in the 2007-08 season batch.
**Decision:** Parse with Python's `csv` module directly and pad/truncate
every row to the header's width, instead of relying on pandas' fixed-width
tokenizer. Verified all extra trailing cells were empty (no real data
truncated) before doing this.

### [Bronze] Design pivot — one-schema-per-league/one-table-per-season hit the Unity Catalog table quota
**What:** the original Bronze design (one schema per league, one table per
season) reached ~470 tables and triggered a Unity Catalog warning at 90% of
the 500-table-per-metastore quota — before Silver or Gold existed. The
design was always going to exceed 500 once Silver/Gold tables were added
(462 main-league season tables + 16 extra-league tables alone is ~478).
**Decision:** dropped all `bronze_*` schemas (see
`01_bronze/00_reset_bronze_schemas.ipynb`) and moved to a leaner design:
Bronze becomes a plain file copy/landing zone (no Delta tables, no Unity
Catalog quota usage), and real tables start at Silver — one table per
league (not per season), built by unioning that league's season files
together. Roughly ~38 Silver tables total (22 main-league divisions + 16
extra leagues) instead of ~470+.
