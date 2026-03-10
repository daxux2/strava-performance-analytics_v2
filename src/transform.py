import pandas as pd
import datetime



df = pd.read_json("data/raw_activities.json")

print(df.head())
print(df.shape)
print(df.columns)


print(df["map"].iloc[0])

print(df)


##Data Transformation and adding some columns

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
df["moving_time_str"] = df["moving_time"].apply(lambda x: str(datetime.timedelta(seconds=int(x))) )


df["ride_duration_category"] = pd.cut(
    df["moving_time_min"],
    bins=[0, 60, 120, 180, 1000],
    labels=["short", "medium", "long", 'epic']
)

df["ride_environment"] = df["sport_type"].map({
    "Ride": "outdoor",
    "VirtualRide": "indoor"
})


df["name"] = "Outdoor Ride"

##Heatmap
df["summary_polyline"] = df["map"].apply(
    lambda x: x.get("summary_polyline") if isinstance(x, dict) else None
)

###Efficiency parameters
df["elevation_per_km"] = df["elevation_m"] / df["distance_km"]
df["efficiency"] = df["avg_speed_kmh"] / df["average_heartrate"]

##Filtrowanie rajdów outdoor z krótkim distance_km oraz nullowyn average_heartrate/average_watts
##df = df[(df["type"] == "Ride") & (df["trainer"] == False)]
df = df[df["distance_km"] > 20]
df.dropna(subset=["average_heartrate"], inplace=True)

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

print(df["map"].iloc[0])

print(df)


##Selecting column
print(df["start_date"].dtypes)
##df = df.set_index("start_date")
df = df.filter(items= [
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
    'summary_polyline',
    'ride_duration_category'

])


print(df)

df.to_csv("data/fact_rides.csv", index=False, sep = ",")
