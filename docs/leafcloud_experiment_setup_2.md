[Previous](/docs/leafcloud_experiment_setup_1.md)

# Database Re-Migration Guide: LEAFCLOUD Phase 1

**Date:** Sunday, January 4, 2026<br>
**Subject:** Transitioning to Normalized Schema

## 1. Overview
Due to the redesign of the database schema (from a monolithic `readings` table to normalized `sensor_data`, `image_data`, `npk_predictions`, and `ground_truth` tables), the existing database and migration history must be reset to ensure consistency and support for data triangulation.

## 2. Re-Migration Procedure

### Step 1: Clear Migration History
Remove the old migration scripts to prevent conflicts with the new schema.
```bash
rm alembic/versions/*.py
```

### Step 2: Reset the Database
Drop the existing tables to allow Alembic to recreate them from scratch using the new `models.py` definitions.
```bash
psql -d leafcloud -c "DROP TABLE IF EXISTS readings, alembic_version CASCADE;"
```

### Step 3: Generate the New Migration
Generate a fresh migration script that reflects the normalized schema.
```bash
alembic revision --autogenerate -m "Phase 1 Redesign: Normalized Tables"
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
*   `sensor_data`
*   `image_data`
*   `npk_predictions`
*   `ground_truth`
*   `alembic_version`

[Next](/docs/leafcloud_experiment_setup_3.md)