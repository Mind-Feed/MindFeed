import argparse

# module, used for creating API service clients.
from googleapiclient.discovery import build
# interface for displaying Web-based documents to users
import webbrowser
# module, commonly used for making HTTP requests
import requests
# module for working with threads
import threading
#Imports the Flask class and the request object from the Flask web framework
from flask import Flask, request

# Creates a Flask web application instance
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
# Starts the thread
flask_thread.start()

# Function to authenticate with Spotify
def authenticate_spotify():
    scope = 'user-read-private user-read-email'
    # URL to authenticate with Spotify using CLIENT_ID, scope and REDIRECT_URI
    auth_url = f'https://accounts.spotify.com/authorize?response_type=code&client_id={CLIENT_ID}&scope={scope}&redirect_uri={REDIRECT_URI}'
     #Opening URL to authenticate with Spotify
    webbrowser.open(auth_url)

# Route for the callback after successful authentication
@app.route('/callback')
def callback():
    global spotify_access_token  # Declare spotify_access_token as a global variable
    code = request.args.get('code') # Retrieves the authorization code from the callback request.
    token_url = 'https://accounts.spotify.com/api/token' #  Defines the Spotify token endpoint URL.
    
    auth_data = { # Defines a dictionary containing data for Spotify token authentication.
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    # Sends a POST request to Spotify to exchange the authorization code for an access token.
    response = requests.post(token_url, data=auth_data)
    # Extracts and stores the Spotify access token.
    spotify_access_token = response.json().get('access_token')
    # Prints a message to indicate that the authentication process is successful.
    print('Authentication with Spotify Successful. You can now search for tracks.')
    # Returns a success message for the Flask route.
    return 'Authentication Successful'

# Function to search and display Spotify tracks
def search_spotify(query):
    # Appends " podcast" to the query to specifically search for podcasts.
    query += " podcast"
    # Defines the headers for the Spotify API request.
    headers = {'Authorization': f'Bearer {spotify_access_token}'}
    # Defines the search endpoint URL for Spotify.
    search_url = f'{SPOTIFY_API_URL}search?q={query}&type=show&limit=10'
    # Sends a GET request to the search endpoint.
    response = requests.get(search_url, headers=headers)

    # Checks if the request was successful.
    if response.status_code == 200:
        # Extracts and displays the name and link of each podcast.
        podcasts = response.json().get('shows', {}).get('items', [])
        # Checks if any podcasts were found.
        if not podcasts:
            print('No podcasts found on Spotify.')
            return

        print('\nSpotify Podcasts Search Results:')
        for podcast in podcasts:
            # Displays the name and link of each podcast.
            print(f"{podcast['name']}")
            print(f"Link: {podcast['external_urls']['spotify']}\n")
    else:
        print('Failed to fetch Spotify data. Please check your input or try again later.')

# Function to search YouTube and display results
def search_youtube(query, max_results=10):
    # Defines the YouTube API client.
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    query += " podcast"
    # Defines the search request for YouTube.
    request = youtube.search().list(
        part='snippet',
        q=query,
        maxResults=max_results,
        type='video',
        videoDuration='long'
    )
    response = request.execute()
    # loops through the search results and displays the title and link of each video.
    for item in response.get('items', []):
        snippet = item.get('snippet', {})
        title = snippet.get('title')
        video_id = item.get('id', {}).get('videoId')
        # Checks if the video has a title and a video ID.
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
        search_query = input("Search podcast: ")
        # Calls the search_youtube function with the search query and max_results
        search_youtube(search_query)
        # Cecks if the Spotify is authenticated
        if spotify_access_token:
            # Calls the search_spotify function with the search query
            search_spotify(search_query)
    elif choice == '2':
        # Calls the authenticate_spotify function
        authenticate_spotify()
    elif choice == '3':
        # Exits the program
        break
    else:
        # Prints an error message if the user enters an invalid choice
        print("Invalid choice. Please enter 1, 2, or 3.")