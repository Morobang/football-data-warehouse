# Databricks notebook source
# MAGIC %md
# MAGIC # Gold — Star schema
# MAGIC
# MAGIC Reads from `workspace.silver.matches`, builds the analysis-ready
# MAGIC star schema:
# MAGIC
# MAGIC     workspace.gold.fact_matches
# MAGIC     workspace.gold.dim_teams
# MAGIC     workspace.gold.dim_leagues
# MAGIC     workspace.gold.dim_seasons
