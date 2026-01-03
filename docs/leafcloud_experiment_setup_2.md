[Previous](/docs/leafcloud_experiment_setup_1.md)

# Database Re-Migration Guide: LEAFCLOUD Phase 2

**Date:** Sunday, January 4, 2026
**Subject:** Transitioning to Production Schema (Version 2.0)

## 1. Overview
The database schema has evolved from a research-focused structure to a production-ready architecture. The old "normalized" tables (`sensor_data`, `image_data`) proved too complex for manual data entry. We are moving to a streamlined structure: `experiments`, `daily_readings`, `lab_results`, and `npk_predictions`.

## 2. Re-Migration Procedure

### Step 1: Clear Migration History
Remove the old migration scripts to prevent conflicts with the new schema.
```bash
rm alembic/versions/*.py
```

### Step 2: Reset the Database
Drop ALL existing tables (Phase 1 and Phase 2 variants) to allow Alembic to recreate them from scratch using the new `models.py` definitions.
```bash
psql -d leafcloud -c "DROP TABLE IF EXISTS readings, sensor_data, image_data, ground_truth, daily_readings, lab_results, experiments, npk_predictions, alembic_version CASCADE;"
```

### Step 3: Generate the New Migration
Generate a fresh migration script that reflects the final production schema.
```bash
alembic revision --autogenerate -m "Phase 2 Redesign: Production Schema"
```

### Step 4: Apply the Migration
Apply the generated changes to the database.
```bash
alembic upgrade head
```

## 3. Verification
After migrating, you can verify the new table structure by listing the tables in PostgreSQL:
```bash
psql -d leafcloud -c "\dt"
```
You should see the following tables:
*   `experiments` (Batch tracker)
*   `daily_readings` (Unified Sensor + Image log)
*   `lab_results` (Ground Truth)
*   `npk_predictions` (AI Output)
*   `alembic_version`

[Next](/docs/leafcloud_experiment_setup_3.md)