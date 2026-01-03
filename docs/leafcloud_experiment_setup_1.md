[Previous](/docs/leafcloud_experiment_setup_0.md)

# Server & Database Redesign Log: LEAFCLOUD Phase 1

**Date:** Saturday, January 3, 2026
**Subject:** Refactoring Server and Database Schema for Experimental Alignment

## 1. Overview
Following an inspection of the project requirements in `LEAFCLOUD.pdf` and the gathering protocol in `leafcloud_experiment_setup.md`, the server architecture and database schema were redesigned. The previous "monolithic" table structure was insufficient for the data triangulation required for CNN training.

## 2. Database Schema Redesign (`models.py`)
The flat `readings` table was decomposed into four normalized tables to support the experimental workflow:

| Table Name | Purpose | Key Columns |
| :--- | :--- | :--- |
| **`sensor_data`** | Stores time-series environmental data. | `timestamp`, `device_id`, `ec`, `ph`, `temp_c` |
| **`image_data`** | Metadata for leaf photos. | `timestamp`, `device_id`, `image_path` |
| **`npk_predictions`** | AI-generated estimates. | `image_id` (FK), `n_ppm`, `p_ppm`, `k_ppm`, `confidence` |
| **`ground_truth`** | **Lab Analysis Results** (Ground Truth). | `timestamp`, `device_id`, `n_actual`, `p_actual`, `k_actual` |

### Key Improvements:
*   **Data Triangulation:** Enabled the ability to link a specific leaf image to both an AI prediction and a Lab result (Ground Truth).
*   **Experimental Tracking:** Switched from `plant_id` to `device_id` to correctly identify the 7 experimental bucket setups.
*   **Regression Support:** Added a specific table for `ground_truth` to facilitate the model training phase.

## 3. Server API Updates (`main.py`)
The FastAPI server was updated to maintain compatibility with the new database structure:

*   **Pydantic Model Realignment:** Reorganized `LatestReadingResponse` to aggregate data from the split tables.
*   **Naming Consistency:** Updated all endpoints to use `device_id` instead of `plant_id`.
*   **Version Bump:** Updated API versioning to `1.1.0`.

## 4. Documentation References
This redesign ensures that the software implementation directly supports the methodology outlined in the **Data Collection Protocol (Section 3)** of the `leafcloud_experiment_setup.md` document, specifically the requirement for 21 lab-verified samples.

[Next](/docs/leafcloud_experiment_setup_2.md)