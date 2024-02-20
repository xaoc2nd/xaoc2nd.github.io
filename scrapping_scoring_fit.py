import os
import requests
import json
from datetime import datetime

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
    # Get today's date
    today_date = datetime.now().strftime('%d/%m/%Y')

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
        event_date_str = item['date']['start']['day']
        # Convert event_date to datetime object
        try:
            event_date_obj = datetime.strptime(event_date_str, '%d/%m/%Y')
        except ValueError:
            # If the date format is not 'DD/MM/YYYY', try 'YYYY-MM-DD'
            event_date_obj = datetime.strptime(event_date_str, '%Y-%m-%d')

        if event_date_obj <= datetime.now():
            # If the event date is not after today's date, skip this competition
            continue

        competition = {
            'id': item['eventNumber'],  # Use 'eventNumber' field for id
            'date': event_date_str,
            'name': item['name'],
            'competitionPicture': item.get('iconLink'),  # Set to None if 'iconLink' is missing
        }
        
        # Fetch event data and add location and formats to the competition
        event_data = get_event_data(item['eventNumber'])  # Use 'eventNumber' as event_id
        if event_data and 'presentation' in event_data:
            presentation_data = event_data['presentation']
            if 'location' in presentation_data:
                competition['location'] = presentation_data['location']
        if event_data and 'leaderboard' in event_data:
            leaderboard_competition_data = event_data['leaderboard']
            if 'divisions' in leaderboard_competition_data:
                divisions = leaderboard_competition_data['divisions']
                formats = [division['name'] for division in divisions]
                competition['formats'] = formats

        # Append competition to competitions list
        competitions.append(competition)

    # Write the updated competitions data to the file
    with open(file_path, 'w') as f:
        json.dump(competitions, f, indent=4)

    print("Data appended to:", file_path)

if __name__ == "__main__":
    main()
