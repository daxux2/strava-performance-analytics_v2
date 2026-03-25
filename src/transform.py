import pandas as pd
import datetime
import polyline



# LOAD DATA
# =========================
df = pd.read_json("data/raw_activities.json")


# BASIC TRANSFORMATIONS
# =========================
df["distance_km"] = df["distance"] / 1000
df["moving_time_min"] = df["moving_time"] / 60
df["moving_time_h"] = df["moving_time"] / 3600
df["avg_speed_kmh"] = df["average_speed"] * 3.6
df["elevation_m"] = df["total_elevation_gain"]

df["start_date"] = pd.to_datetime(df["start_date"])
df["year"] = df["start_date"].dt.year
df["month"] = df["start_date"].dt.month
df["week"] = df["start_date"].dt.isocalendar().week
df["weekday"] = df["start_date"].dt.day_name()
df["start_hour"] = df["start_date"].dt.hour

df["moving_time_str"] = df["moving_time"].apply(
    lambda x: str(datetime.timedelta(seconds=int(x)))
)

df["ride_duration_category"] = pd.cut(
    df["moving_time_min"],
    bins=[0, 60, 120, 180, 1000],
    labels=["short", "medium", "long", "epic"]
)

df["ride_environment"] = df["sport_type"].map({
    "Ride": "outdoor",
    "VirtualRide": "indoor"
})

df["name"] = "Outdoor Ride"


# POLYLINE (GEO)
# =========================
df["summary_polyline"] = df["map"].apply(
    lambda x: x.get("summary_polyline") if isinstance(x, dict) else None
)


# METRICS
# =========================
df["elevation_per_km"] = df["elevation_m"] / df["distance_km"]
df["efficiency"] = df["avg_speed_kmh"] / df["average_heartrate"]


# FILTERING
# =========================
df = df[df["distance_km"] > 20]
df = df.dropna(subset=["average_heartrate"])


# BUILD GEO TABLE (NOWE)
# =========================
def build_ride_points(df):
    points = []

    for _, row in df.iterrows():
        poly = row["summary_polyline"]

        if pd.notnull(poly):
            try:
                coords = polyline.decode(poly)

                # 🔥 kluczowe dla wydajności
                coords = coords[::5]

                for i, (lat, lon) in enumerate(coords):
                    points.append({
                        "ride_id": row["id"],
                        "point_order": i,
                        "lat": lat,
                        "lon": lon,
                        "year": row["year"],
                        "month": row["month"]
                    })

            except Exception as e:
                print(f"Polyline error for ride {row['id']}: {e}")

    return pd.DataFrame(points)

df_points = build_ride_points(df)


# SELECT FINAL COLUMNS
# =========================
df_rides = df.filter(items=[
    'id',
    "ride_environment",
    'start_date',
    'year',
    'month',
    "week",
    'weekday',
    'distance_km',
    'total_elevation_gain',
    "moving_time_str",
    'moving_time_min',
    'avg_speed_kmh',
    'elevation_per_km',
    'efficiency',
    'average_heartrate',
    'max_heartrate',
    'ride_duration_category',
    'average_watts'
])


# =========================
# SAVE
# =========================
df_rides.to_csv("data/fact_rides.csv", index=False)
df_points.to_csv("data/ride_points.csv", index=False)


print("✅ ETL completed")
print(f"Rides: {df_rides.shape}")
print(f"Points: {df_points.shape}")

print(df_rides)