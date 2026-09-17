from pathlib import Path

import pandas as pd

from src.database.connection import get_connection


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_FOLDER = PROJECT_ROOT / "data" / "processed"


def load_data():

    # Read processed CSV files
    traffic = pd.read_csv(
        PROCESSED_FOLDER / "traffic_clean.csv"
    )

    parking = pd.read_csv(
        PROCESSED_FOLDER / "parking_clean.csv"
    )

    traffic_observations = pd.read_csv(
        PROCESSED_FOLDER / "traffic_observations.csv"
    )

    parking_observations = pd.read_csv(
        PROCESSED_FOLDER / "parking_observations.csv"
    )


    # Connect to PostgreSQL
    conn = get_connection()

    cursor = conn.cursor()


    # -------------------------
    # CURRENT TRAFFIC DATA
    # -------------------------

    cursor.execute("DELETE FROM traffic_locations")

    for _, row in traffic.iterrows():

        cursor.execute(
            """
            INSERT INTO traffic_locations
            (
                sensor_id,
                road_name,
                direction,
                lat,
                lng,
                period,
                flow,
                speed,
                road_id,
                offset,
                collected_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                row["sensor_id"],
                row["road_name"],
                row["direction"],
                row["lat"],
                row["lng"],
                row["period"],
                row["flow"],
                row["speed"],
                row["road_id"],
                row["offset"],
                row["collected_at"]
            )
        )


    # -------------------------
    # CURRENT PARKING DATA
    # -------------------------

    cursor.execute("DELETE FROM parking_locations")

    for _, row in parking.iterrows():

        cursor.execute(
            """
            INSERT INTO parking_locations
            (
                name,
                id,
                status,
                total,
                free,
                tendance,
                lat,
                lng,
                collected_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                row["name"],
                row["id"],
                row["status"],
                row["total"],
                row["free"],
                row["tendence"],
                row["lat"],
                row["lng"],
                row["collected_at"]
            )
        )


    # -------------------------
    # TRAFFIC HISTORY
    # -------------------------

    for _, row in traffic_observations.iterrows():

        cursor.execute(
            """
            INSERT INTO traffic_observations
            (
                sensor_id,
                direction,
                offset,
                period,
                flow,
                speed,
                collected_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                row["sensor_id"],
                row["direction"],
                row["offset"],
                row["period"],
                row["flow"],
                row["speed"],
                row["collected_at"]
            )
        )


    # -------------------------
    # PARKING HISTORY
    # -------------------------

    for _, row in parking_observations.iterrows():

        cursor.execute(
            """
            INSERT INTO parking_observations
            (
                parking_id,
                status,
                free,
                tendance,
                collected_at
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                row["parking_id"],
                row["status"],
                row["free"],
                row["tendence"],
                row["collected_at"]
            )
        )


    # Save changes
    conn.commit()

    cursor.close()
    conn.close()

    print("Data loaded successfully into PostgreSQL.")


if __name__ == "__main__":
    load_data()