import argparse
from googleapiclient.discovery import build
import webbrowser
import requests
import threading
from flask import Flask, request

app = Flask(__name__)

# YouTube API key
YOUTUBE_API_KEY = 'AIzaSyCJrBa4FuRoZ7j4rOiPS5VRPHEQPK7NLHQ'

# Spotify API credentials
CLIENT_ID = '3dbfa5b09ce546448990687751ad470e'
CLIENT_SECRET = '142444ed089049a6bed24c4000c74708'
REDIRECT_URI = 'http://localhost:5000/callback'
SPOTIFY_API_URL = 'https://api.spotify.com/v1/'

# Variable to store the access token
spotify_access_token = ''

# Function to start Flask app in a separate thread
def run_flask_app():
    app.run(debug=False)

# Start Flask app in a separate thread
flask_thread = threading.Thread(target=run_flask_app)
flask_thread.start()

# Function to authenticate with Spotify
def authenticate_spotify():
    scope = 'user-read-private user-read-email'
    auth_url = f'https://accounts.spotify.com/authorize?response_type=code&client_id={CLIENT_ID}&scope={scope}&redirect_uri={REDIRECT_URI}'
    webbrowser.open(auth_url)

# Route for the callback after successful authentication
@app.route('/callback')
def callback():
    global spotify_access_token  # Declare spotify_access_token as a global variable
    code = request.args.get('code')
    token_url = 'https://accounts.spotify.com/api/token'
    auth_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    response = requests.post(token_url, data=auth_data)
    spotify_access_token = response.json().get('access_token')
    print('Authentication with Spotify Successful. You can now search for tracks.')
    return 'Authentication Successful'

# Function to search and display Spotify tracks
def search_spotify(query):
    query += " podcast"
    headers = {'Authorization': f'Bearer {spotify_access_token}'}
    search_url = f'{SPOTIFY_API_URL}search?q={query}&type=show&limit=10'
    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        podcasts = response.json().get('shows', {}).get('items', [])
        if not podcasts:
            print('No podcasts found on Spotify.')
            return

        print('\nSpotify Podcasts Search Results:')
        for podcast in podcasts:
            print(f"{podcast['name']}")
            print(f"Link: {podcast['external_urls']['spotify']}\n")
    else:
        print('Failed to fetch Spotify data. Please check your input or try again later.')

# Function to search YouTube and display results
def search_youtube(query, max_results=10):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    query += " podcast"

    request = youtube.search().list(
        part='snippet',
        q=query,
        maxResults=max_results,
        type='video',
        videoDuration='long'
    )

    response = request.execute()

    print('\nYouTube Search Results (Videos longer than 20 minutes):')
    for item in response.get('items', []):
        snippet = item.get('snippet', {})
        title = snippet.get('title')
        video_id = item.get('id', {}).get('videoId')

        if title and video_id:
            link = f'https://www.youtube.com/watch?v={video_id}'
            print(f'Title: {title}')
            print(f'Link: {link}\n')

# Main loop
while True:
    print("\nMenu:")
    print("1. Search on YouTube and Spotify")
    print("2. Authenticate with Spotify")
    print("3. Exit")

    choice = input("Enter your choice (1/2/3): ")

    if choice == '1':
        search_query = input("Enter your search query: ")
        search_youtube(search_query)
        if spotify_access_token:
            search_spotify(search_query)
    elif choice == '2':
        authenticate_spotify()
    elif choice == '3':
        break
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")