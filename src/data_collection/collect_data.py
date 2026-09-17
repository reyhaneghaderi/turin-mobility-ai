import os
import requests
import psycopg2
import xml.etree.ElementTree as ET

from datetime import datetime
from dotenv import load_dotenv


# --------------------------------------------------
# 1. LOAD DATABASE SETTINGS
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# 2. CONNECT TO POSTGRESQL
# --------------------------------------------------

connection = psycopg2.connect(
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

cursor = connection.cursor()

print("Connected to PostgreSQL")


# --------------------------------------------------
# 3. COLLECTION TIME
# --------------------------------------------------

collected_at = datetime.now().replace(microsecond=0)


# ==================================================
# PARKING DATA
# ==================================================

parking_url = "https://opendata.5t.torino.it/get_pk"

response = requests.get(parking_url, timeout=30)

parking_root = ET.fromstring(response.content)


parking_count = 0


for record in list(parking_root)[1:]:

    data = record.attrib

    parking_id = int(data.get("ID"))
    status = int(data.get("status"))
    tendence = int(data.get("tendence"))

    free = data.get("Free")

    # Some parking locations have missing Free values
    if free is not None and free != "":
        free = int(float(free))
    else:
        free = None


    cursor.execute(
        """
        INSERT INTO parking_observations
        (parking_id, status, free, tendence, collected_at)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            parking_id,
            status,
            free,
            tendence,
            collected_at
        )
    )

    parking_count += 1


print("Parking data prepared:", parking_count, "records")


# ==================================================
# TRAFFIC DATA
# ==================================================

traffic_url = "https://opendata.5t.torino.it/get_fdt"

response = requests.get(traffic_url, timeout=30)

traffic_root = ET.fromstring(response.content)


traffic_count = 0


for record in list(traffic_root)[1:]:

    road = record.attrib

    traffic = list(record)[0].attrib


    sensor_id = road.get("lcd1")

    direction = road.get("direction")

    offset = int(road.get("offset"))

    period = int(road.get("period"))

    flow = int(float(traffic.get("flow")))

    speed = float(traffic.get("speed"))


    cursor.execute(
        """
        INSERT INTO traffic_observations
        (sensor_id, direction, "offset", period, flow, speed, collected_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (
            sensor_id,
            direction,
            offset,
            period,
            flow,
            speed,
            collected_at
        )
    )

    traffic_count += 1


print("Traffic data prepared:", traffic_count, "records")


# --------------------------------------------------
# 4. SAVE EVERYTHING TO POSTGRESQL
# --------------------------------------------------

connection.commit()

print("--------------------------------")
print("Parking data saved:", parking_count)
print("Traffic data saved:", traffic_count)
print("Collection time:", collected_at)
print("--------------------------------")


# --------------------------------------------------
# 5. CLOSE DATABASE CONNECTION
# --------------------------------------------------

cursor.close()
connection.close()

print("Database connection closed")

