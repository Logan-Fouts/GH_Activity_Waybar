import requests
from dotenv import load_dotenv
import os
from datetime import date, datetime, timedelta
import json

load_dotenv()

def main():
    username = os.getenv("USERNAME_New")
    github_token = os.getenv("GITHUB_TOKEN")

    if not username or not github_token:
        print(json.dumps({"text": "Error: Missing USERNAME or GITHUB_TOKEN", "tooltip": "Check your .env file"}))
        exit(1)

    events = fetch_events(username, github_token)
    build_activity_calendar(events)

def fetch_events(username, github_token):
    url = f"https://api.github.com/users/{username}/events"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {github_token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(json.dumps({"text": f"Error: {response.status_code}", "tooltip": response.text}))
        exit(1)

    return response.json()

def build_activity_calendar(events):
    previous_week = [False] * 7

    today = date.today()

    for event in events:
        event_date = datetime.fromisoformat(event["created_at"].replace("Z", "")).date()
        
        delta = (today - event_date).days
        
        if 0 <= delta < 7:
            previous_week[delta] = True

    previous_week.reverse()
    activity_graph = "".join(["🟩" if active else "⬛" for active in previous_week])
    text = f"{activity_graph}"
    tooltip = "GitHub contribution activity over the last 7 days"
    print(json.dumps({"text": text, "tooltip": tooltip}))

if __name__ == "__main__":
    main()