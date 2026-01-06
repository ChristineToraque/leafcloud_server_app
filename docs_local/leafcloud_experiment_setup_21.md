[Previous](/docs/leafcloud_experiment_setup_20.md)

# API Testing Guide & Sample Data

**Date:** Monday, January 5, 2026<br>
**Subject:** Standardizing API Testing Procedures

## 1. Action Taken
Created a comprehensive guide for testing API endpoints using `curl`, ensuring consistent validation of Authentication, IoT uploads, and Mobile App data retrieval.

## 2. Implementation Details

### A. Base URL
*   **Local Environment:** `http://localhost:8000`

### B. Authentication
*   **Endpoint:** `POST /auth/login`
*   **Credentials:**
    *   **Email:** `admin@leafcloud.com`
    *   **Password:** `admin`
*   **Sample Command:**
    ```bash
    curl -X POST http://localhost:8000/auth/login \
         -H "Content-Type: application/json" \
         -d '{"email": "admin@leafcloud.com", "password": "admin"}'
    ```

### C. IoT Data Simulation (Raspberry Pi)
*   **Endpoint:** `POST /iot/upload_data/`
*   **Purpose:** Simulates sensor readings and image uploads from the edge device.
*   **Sample Command:**
    ```bash
    curl -X POST http://localhost:8000/iot/upload_data/ \
         -F "image=@path/to/test_image.jpg" \
         -F "ph=6.2" \
         -F "ec=1.8" \
         -F "temp=22.5" \
         -F "bucket_label=Bucket-A-21"
    ```

### D. Mobile App Data Retrieval
*   **Latest Status:** `GET /app/latest_status/`
*   **History:** `GET /app/history/?limit=10`
*   **Alerts:** `GET /app/alerts/`

### E. Validation Scenarios
*   **Optimal Growth:** pH 6.0, EC 1.5 -> "Optimal"
*   **pH Lockout:** pH 4.5 -> "Critical Warning"
*   **Low Nitrogen:** AI Prediction < 100ppm -> "Deficiency Alert"

## 3. Current State
The API is fully functional and documented. Manual testing via `curl` confirms all endpoints are responding correctly with JSON payloads.

## 4. Next Steps
*   **Automation:** Create a Python script to run these tests automatically in the CI/CD pipeline.
*   **Staging:** Deploy the server to a staging environment for remote mobile app testing.

[Next](/docs/leafcloud_experiment_setup_22.md)
