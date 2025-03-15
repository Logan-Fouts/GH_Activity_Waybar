import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import json

load_dotenv()

def main():
    username = os.getenv("USERNAME")
    github_token = os.getenv("GITHUB_TOKEN")

   
    if not username or not github_token:
        print(json.dumps({"text": "Error: Missing USERNAME or GITHUB_TOKEN", "tooltip": "Check your .env file"}))
        exit(1)

  
    events = fetch_events(username, github_token)

   
    activity_graph = generate_activity_graph(events)

    
    text = f"{activity_graph}"
    tooltip = "Github contribution activity over the last 7 days"

    
    print(json.dumps({"text": text, "tooltip": tooltip}))

def fetch_events(username, github_token):
    url = f"https://api.github.com/users/{username}/received_events/public"
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

def generate_activity_graph(events):
    now = datetime.utcnow()
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    activity = {day: False for day in days_of_week}

    for event in events:
        created_at = event["created_at"] 
        event_time = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")  
 
        if (now - event_time).days <= 7:
            day_of_week = event_time.strftime("%A")  
            activity[day_of_week] = True 

    activity_graph = "".join(["🟩" if activity[day] else "⬛" for day in days_of_week])
    return activity_graph

if __name__ == "__main__":
    main()