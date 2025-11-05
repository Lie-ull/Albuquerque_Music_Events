from flask import Flask, render_template
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Get API key from environment variable
API_KEY = os.getenv('TICKETMASTER_API_KEY')

# Ticketmaster API base URL
BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"


def get_music_events():
    """
    Fetch music events in Albuquerque for the next 6 months from Ticketmaster API
    Returns: List of event dictionaries with relevant information
    """

    # Calculate date range: today to 6 months from now
    start_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    end_date = (datetime.now() + timedelta(days=180)).strftime('%Y-%m-%dT%H:%M:%SZ')

    # ===== YOUR CODE HERE =====
    # TODO: Create the params dictionary for the API request
    # What you're coding: API request parameters
    # What it does: Tells Ticketmaster API what events to search for
    # Hints:
    # - Include 'apikey' with the API_KEY variable
    # - Set 'city' to "Albuquerque"
    # - Set 'stateCode' to "NM"
    # - Set 'classificationName' to "Music" (to filter only music events)
    # - Set 'startDateTime' to start_date
    # - Set 'endDateTime' to end_date
    # - Set 'size' to 200 (max results per request)
    # - Set 'sort' to "date,asc" (sort by date, ascending)
    params = {
        'apikey': API_KEY,
        'city': 'Albuquerque',
        'stateCode': "NM",
        'classificationName': "Music",
        'startDateTime': start_date,
        'endDateTime': end_date,
        'size': 200,
        'sort': 'date,asc'
    }

    try:
        # Make API request to Ticketmaster
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()

        data = response.json()

        # Check if events exist in the response
        if '_embedded' not in data or 'events' not in data['_embedded']:
            return []

        events = []

        # ===== YOUR CODE HERE =====
        # TODO: Loop through each event in data['_embedded']['events']
        # What you're coding: Event data extraction loop
        # What it does: Processes each event and extracts key information
        # Hints:
        # - Use a for loop: for event in data['_embedded']['events']:
        # - Inside the loop, create a dictionary with event details
        # - Extract: name, date, time, venue name, address, image URL, ticket URL
        # - Check if keys exist before accessing (use .get() method)
        # - For the date, extract 'localDate' from event['dates']['start']
        # - For the time, extract 'localTime' from event['dates']['start']
        # - For venue, use event['_embedded']['venues'][0]['name']
        # - For address, use event['_embedded']['venues'][0]['address']['line1']
        # - For image, use event['images'][0]['url'] if images exist
        # - For URL, use event['url']
        # - Append each event dictionary to the events list

        # Your loop code here
        for event in data['_embedded']['events']:
            event_info = {
                'name': event.get('name', 'No name'),
                'date': event['dates']['start']['localDate'],
                'time': event['dates']['start']['localTime'],
                'venue': event['_embedded']['venues'][0].get('name', "no name"),
                'address': event['_embedded']['venues'][0]['address'].get('line1', "Address TBA"),
                'image': event['images'][0]['url'],
                'url': event.get('url', '#')
            }
            events.append(event_info)
        # ==========================

        return events

    except requests.exceptions.RequestException as e:
        print(f"Error fetching events: {e}")
        return []


def format_date(date_string):
    """
    Format date string to be more readable
    Example: 2025-11-15 becomes "Sat, Nov 15, 2025"
    """
    try:
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        return date_obj.strftime('%a, %b %d, %Y')
    except:
        return date_string


# Make format_date available in templates
app.jinja_env.filters['format_date'] = format_date


@app.route('/')
def index():
    """
    Main route - fetches events and renders the homepage
    Everything happens in Python - no JavaScript needed!
    """
    # Get all music events
    events = get_music_events()

    # Pass events to the template
    # The template will loop through events and display them
    return render_template('index_python.html', events=events)


if __name__ == '__main__':
    # Run the Flask development server
    app.run(debug=True, host='0.0.0.0', port=5000)