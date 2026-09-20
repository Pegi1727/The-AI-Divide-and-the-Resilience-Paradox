# SQL Reproducibility Layer

This directory contains the relational database implementation for the study
"The AI Divide and the Resilience Paradox."

## Files

1. `01_schema_ddl.sql`  
   Creates the research table, constraints, and indexes.

2. `02_data_seed.sql`  
   Inserts the 60 empirical observations used in the study.

3. `03_analytical_views.sql`  
   Creates standardized, stratified, and aggregated analytical views.

4. `04_statistical_queries.sql`  
   Computes descriptive statistics, Pearson correlations, and access-tier
   comparisons using SQL.

## Execution Order

Run the files in numerical order:
```bash
sqlite3 ai_resilience.db < 01_schema_ddl.sql
sqlite3 ai_resilience.db < 02_data_seed.sql
sqlite3 ai_resilience.db < 03_analytical_views.sql
sqlite3 ai_resilience.db < 04_statistical_queries.sql
