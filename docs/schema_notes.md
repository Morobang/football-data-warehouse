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

## Example entry (replace once real issues are found)

### [Bronze] Column count mismatch, older vs recent seasons
**What:** 2005-06 season files have far fewer betting-odds columns than
2025-26 files (bookmakers have added markets over time).
**Where:** All main leagues, most visible in England E0.
**Decision:** TBD — likely keep only the core columns present across all
seasons in Silver, rather than trying to backfill missing odds columns for
older data.
