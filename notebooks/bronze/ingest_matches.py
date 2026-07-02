# Databricks notebook source
# MAGIC %md
# MAGIC # Bronze — Ingest raw CSVs
# MAGIC
# MAGIC Reads every raw CSV under the Volume, tags each row with source
# MAGIC metadata (country, division, season) extracted from the file PATH
# MAGIC (not the CSV contents), and writes to a Delta table:
# MAGIC
# MAGIC     workspace.bronze.matches
# MAGIC
# MAGIC No cleaning here — this layer is "as-is, but traceable to its source."
