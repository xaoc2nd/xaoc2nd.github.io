import os
import time
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

def get_competitions(timestamp):
    url = 'https://competitioncorner.net/api2/v1/events/filtered'
    params = {
        'timing': 'active',
        'timestamp': timestamp,
        'format': 'team',
        'type': 'functional_fitness',
        'countryIds': [73, 40, 6, 19],  # List of country IDs
        'page': 1,
        'perPage': 10
    }

    competitions = []

    try:
        while True:
            response = make_api_call(url, params=params)
            if not response:
                print("API call failed or returned empty JSON.")
                break
            
            if not response:
                print("API returned empty JSON. Terminating loop.")
                break
            
            for event in response:
                competition = {
                    'id': event['id'],
                    'name': event['name'],
                    'location': event['locationTitle'],
                    'date': event['startDateTime']
                }
                competitions.append(competition)
                
            params['page'] += 1
    except KeyboardInterrupt:
        print("Keyboard interrupt received. Terminating.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return competitions

def get_competition_picture(event_id):
    url = f'https://competitioncorner.net/api2/v1/registrationinfo/event/{event_id}/divisions'
    response = make_api_call(url)
    if response and 'visualSettings' in response and 'logoImage' in response['visualSettings']:
        return response['visualSettings']['logoImage']
    return None

def main():
    timestamp = int(time.time() * 1000)  # Replace this with your actual timestamp
    competitions = get_competitions(timestamp)

    if competitions:
        for competition in competitions:
            competition['competitionPicture'] = get_competition_picture(competition['id'])

        # Define the file path
        file_path = "data/getCompetitions/competitions.json"

        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Write the JSON data to the file with indentation for readability
        with open(file_path, 'w') as f:
            json.dump(competitions, f, indent=4)

        print("Data saved to:", file_path)
    else:
        print("No competitions found.")

if __name__ == "__main__":
    main()
