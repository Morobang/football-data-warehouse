# Databricks notebook source
# MAGIC %md
# MAGIC # Silver — Clean and standardize
# MAGIC
# MAGIC Reads from `workspace.bronze.matches`, reconciles schema drift
# MAGIC (see ../../docs/schema_notes.md for what's actually found),
# MAGIC standardizes team names, and writes to:
# MAGIC
# MAGIC     workspace.silver.matches
