import requests
from config import ACCESS_TOKEN


def get_activities(per_page=10):
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    params = {"per_page": per_page}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(response.json())
        raise Exception("API request failed")

    return response.json()


def main():
    activities = get_activities(10)
    print(f"Downloaded {len(activities)} activities")


if __name__ == "__main__":
    main()