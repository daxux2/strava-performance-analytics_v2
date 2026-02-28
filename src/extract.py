import requests
import json
import os
from config import ACCESS_TOKEN


def get_all_activities():
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    all_activities = []
    page = 1

    while True:
        params = {
            "per_page": 200,
            "page": page
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print("STATUS:", response.status_code)
            print("RESPONSE:", response.text)
            raise Exception("API request failed")

        activities = response.json()

        if not activities:
            break

        print(f"Downloaded page {page} ({len(activities)} activities)")
        all_activities.extend(activities)

        page += 1

    return all_activities


def main():
    activities = get_all_activities()

    os.makedirs("data", exist_ok=True)

    with open("data/raw_activities.json", "w", encoding="utf-8") as f:
        json.dump(activities, f, indent=4)

    print(f"Total downloaded: {len(activities)} activities")

    print(f"Downloaded {len(activities)} activities")
    print("Saved to data/raw_activities.json")


if __name__ == "__main__":
    main()