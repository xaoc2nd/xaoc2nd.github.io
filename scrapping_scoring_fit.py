import os
import requests
import json

def make_api_call(url, params=None):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error making API call: {e}")
        return None

def get_leaderboard_data():
    url = 'https://scoring-rsnatch-prod.herokuapp.com/api/leaderboard/competition/all'
    data = make_api_call(url)
    if data and 'competitions' in data:
        return data['competitions']
    return None

def get_event_data(event_id):
    url = f'https://scoring-rsnatch-prod.herokuapp.com/api/event/presentation/{event_id}'
    data = make_api_call(url)
    return data

def main():
    # Get existing competitions data
    file_path = "data/getCompetitions/competitions.json"
    try:
        with open(file_path, 'r') as f:
            competitions = json.load(f)
    except FileNotFoundError:
        print("Error: Competitions file not found.")
        return
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in the competitions file.")
        return

    # Fetch leaderboard data
    leaderboard_data = get_leaderboard_data()
    if not leaderboard_data:
        print("Error: Failed to fetch leaderboard data or missing 'competitions' field.")
        return

    # Process leaderboard data and append to competitions
    for item in leaderboard_data:
        competition = {
            'id': item['_id'],
            'date': item['date']['start']['day'],
            'name': item['name'],
            'competitionPicture': item.get('iconLink')  # Set to None if 'iconLink' is missing
        }
        
        # Fetch event data and add leaderboard divisions to the competition format field
        event_data = get_event_data(item['_id'])
        if event_data and 'divisions' in event_data:
            divisions_names = [division['name'] for division in event_data['divisions']]
            competition['format'] = divisions_names

        # Append competition to competitions list
        competitions.append(competition)

    # Write the updated competitions data to the file
    with open(file_path, 'w') as f:
        json.dump(competitions, f, indent=4)

    print("Data appended to:", file_path)

if __name__ == "__main__":
    main()
