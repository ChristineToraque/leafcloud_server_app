# LEAFCLOUD API

This is the backend API for the LEAFCLOUD Hydroponics Monitoring System. It provides endpoints to retrieve sensor readings, system status, and recommendations for hydroponic plant care.

## Features

*   **Latest Readings**: Get real-time sensor data (EC, pH, Temp) and system predictions.
*   **History**: Retrieve historical data for charting and analysis.
*   **Database Integration**: Uses PostgreSQL with SQLAlchemy and Alembic for migrations.

## Prerequisites

Before you begin, ensure you have the following installed:

*   **Python 3.8+**
*   **PostgreSQL** (and a running server instance)

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd leafcloud_server_miming
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.text
    ```

## Database Setup

1.  **Create the PostgreSQL database:**

    Ensure you have a PostgreSQL user and database ready. For example:

    ```sql
    CREATE DATABASE leafcloud;
    ```

2.  **Configure Database URL:**

    Create a copy of the example configuration file and name it `alembic.ini`.

    ```bash
    cp alembic.ini.example alembic.ini
    ```

    Now, open the new `alembic.ini` file and update the `sqlalchemy.url` line with your database credentials:

    ```ini
    # alembic.ini
    sqlalchemy.url = postgresql://<username>:<password>@localhost/leafcloud
    ```

3.  **Run Migrations:**

    Apply the database schema:

    ```bash
    alembic upgrade head
    ```

## Running the Server

You can run the server using Python directly or via Uvicorn.

**Option 1: Direct Python execution**
```bash
python main.py
```

**Option 2: Using Uvicorn (Recommended for development)**
```bash
uvicorn main:app --reload
```

The server will start at `http://0.0.0.0:8000`.

## API Documentation

Once the server is running, you can access the interactive API documentation:

*   **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
*   **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Project Structure

*   `main.py`: The entry point for the FastAPI application.
*   `models.py`: SQLAlchemy database models.
*   `database.py`: Database connection setup.
*   `alembic/`: Database migration scripts.
*   `requirements.text`: Python dependencies.
