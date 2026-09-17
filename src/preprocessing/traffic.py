from pathlib import Path
import xml.etree.ElementTree as ET
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

traffic_path = PROJECT_ROOT / "data" / "raw" / "traffic.xml"


tree = ET.parse(traffic_path)
root = tree.getroot()


rows = []

for record in list(root)[1:]:

    road = record.attrib
    traffic = list(record)[0].attrib

    rows.append({
        "sensor_id": road.get("lcd1"),
        "road_name": road.get("Road_name"),
        "direction": road.get("direction"),
        "lat": road.get("lat"),
        "lng": road.get("lng"),
        "period": road.get("period"),
        "flow": traffic.get("flow"),
        "speed": traffic.get("speed"),
        "road_id": road.get("Road_LCD"),
        "offset": road.get("offset")
    })


df = pd.DataFrame(rows)


df["sensor_id"] = df["sensor_id"].astype(str)
df["road_id"] = df["road_id"].astype(str)

df["offset"] = pd.to_numeric(df["offset"])


df_float = ["lat", "lng", "speed"]

for col in df_float:
    df[col] = df[col].astype(float)


df_int = ["period", "flow"]

for col in df_int:
    df[col] = df[col].astype(int)


collected_at = pd.Timestamp.now()

df["collected_at"] = collected_at


output_path = PROJECT_ROOT / "data" / "processed" / "traffic_clean.csv"

output_path.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(output_path, index=False)


print(df.head())
print("Traffic shape:", df.shape)