import os
import time
import requests
import json

def make_api_call(timestamp, page):
    url = 'https://competitioncorner.net/api2/v1/events/filtered'
    params = {
        'timing': 'active',
        'timestamp': timestamp,
        'format': 'team',
        'type': 'functional_fitness',
        'countryIds': [73, 40, 6, 19],  # List of country IDs
        'page': page,
        'perPage': 10
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        filtered_data=[]
        for event in data:
            filtered_event = {
                'id': event['id'],
                'name': event['name'],
                'locationTitle': event['locationTitle'],
                'startDateTime': event['startDateTime']
            }
            filtered_data.append(filtered_event)
        return filtered_data
    except requests.exceptions.RequestException as e:
        print(f"Error making API call: {e}")
        return None

def main():
    timestamp = int(time.time() * 1000)  # Replace this with your actual timestamp
    page = 1
    all_results = []
    while True:
        result = make_api_call(timestamp, page)
        
        if not result:  # If API call fails or returns empty JSON
            print("API call failed or returned empty JSON.")
            break
        
        if not result:  # If API returns an empty JSON array
            print("API returned empty JSON. Terminating loop.")
            break
        all_results.extend(result)  # Append current page results to the list
        page += 1  # Increment page number for the next iteration
    json_result = json.dumps(all_results)
    file_path = "data/getCompetitions/competitions.json"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(json_result)
    print("Data saved to:", file_path)


if __name__ == "__main__":
    main()
