# Databricks notebook source
# MAGIC %md
# MAGIC # Gold — Star schema
# MAGIC
# MAGIC Silver is one table per league (`workspace.silver.england_premier_league`,
# MAGIC `workspace.silver.england_championship`, etc. - see docs/schema_notes.md),
# MAGIC not a single `workspace.silver.matches` table. This notebook will need to
# MAGIC UNION ALL of them (each already carries `source_season`; will need a
# MAGIC `source_league`/`source_country` tag added per table too) before building
# MAGIC the analysis-ready star schema:
# MAGIC
# MAGIC     workspace.gold.fact_matches
# MAGIC     workspace.gold.dim_teams
# MAGIC     workspace.gold.dim_leagues
# MAGIC     workspace.gold.dim_seasons
# MAGIC
# MAGIC Not started - wait until all per-league Silver tables exist.
