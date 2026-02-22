import requests
import json
import os
from config import ACCESS_TOKEN


def get_activities(per_page=10):
    url = "https://www.strava.com/api/v3/athlete/activities"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    params = {
        "per_page": per_page
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print("Status code:", response.status_code)
        print(response.text)
        raise Exception("API request failed")

    return response.json()


def main():
    activities = get_activities(10)

    # tworzy folder data jeśli nie istnieje
    os.makedirs("data", exist_ok=True)

    # zapis surowych danych
    with open("data/raw_activities.json", "w", encoding="utf-8") as f:
        json.dump(activities, f, indent=4)

    print(f"Downloaded {len(activities)} activities")
    print("Saved to data/raw_activities.json")


if __name__ == "__main__":
    main()