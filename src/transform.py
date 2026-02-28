import pandas as pd

df = pd.read_json("data/raw_activities.json")

print(df.head())
print(df.columns)