import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import json

# Load environment variables
load_dotenv()

def main():
    username = os.getenv("USERNAME")
    github_token = os.getenv("GITHUB_TOKEN")

    # Check if environment variables are set
    if not username or not github_token:
        print(json.dumps({"text": "Error: Missing USERNAME or GITHUB_TOKEN", "tooltip": "Check your .env file"}))
        exit(1)

    # Fetch GitHub events
    events = fetch_events(username, github_token)

    # Generate the activity graph
    activity_graph = generate_activity_graph(events)

    # Format the output for Waybar
    text = f"GitHub Activity: {activity_graph}"
    tooltip = "Days with activity: 🟩, Days without activity: ⬛"

    # Output JSON for Waybar
    print(json.dumps({"text": text, "tooltip": tooltip}))

def fetch_events(username, github_token):
    url = f"https://api.github.com/users/{username}/received_events/public"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {github_token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    # Make the API request
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        print(json.dumps({"text": f"Error: {response.status_code}", "tooltip": response.text}))
        exit(1)

    # Return the JSON response
    return response.json()

def generate_activity_graph(events):
    now = datetime.utcnow()
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    activity = {day: False for day in days_of_week}  # Initialize all days as inactive

    # Process each event
    for event in events:
        created_at = event["created_at"]  # Get the "created_at" field
        event_time = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")  # Convert to datetime object
        # Check if the event is within the last 7 days
        if (now - event_time).days <= 7:
            day_of_week = event_time.strftime("%A")  # Get the day of the week
            activity[day_of_week] = True  # Mark the day as active

    # Generate the activity graph
    activity_graph = "".join(["🟩" if activity[day] else "⬛" for day in days_of_week])
    return activity_graph

if __name__ == "__main__":
    main()