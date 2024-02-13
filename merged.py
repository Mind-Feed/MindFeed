import tkinter as tk
from tkinter import ttk, messagebox
from flask import request
import requests
import webbrowser
from googleapiclient.discovery import build
import threading

app = tk.Tk()
app.title("Music App")

# Spotify API credentials
CLIENT_ID = '3dbfa5b09ce546448990687751ad470e'
CLIENT_SECRET = '142444ed089049a6bed24c4000c74708'
REDIRECT_URI = 'http://localhost:5000/callback'
SPOTIFY_API_URL = 'https://api.spotify.com/v1/'

# YouTube API key
YOUTUBE_API_KEY = 'YOUR_YOUTUBE_API_KEY'  # Replace with your actual YouTube API key

# Variable to store the Spotify access token
access_token = ''

# Function to start Flask app in a separate thread
def run_flask_app():
    app.run(debug=False)

# Start Flask app in a separate thread
flask_thread = threading.Thread(target=run_flask_app)
flask_thread.start()

# Function to authenticate with Spotify
def authenticate():
    scope = 'user-read-private user-read-email'
    auth_url = f'https://accounts.spotify.com/authorize?response_type=code&client_id={CLIENT_ID}&scope={scope}&redirect_uri={REDIRECT_URI}'
    webbrowser.open(auth_url)

# Route for the callback after successful Spotify authentication
@app.route('/callback')
def callback():
    global access_token  # Declare access_token as a global variable
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
    access_token = response.json().get('access_token')
    messagebox.showinfo('Authentication Successful', 'You have successfully authenticated with Spotify!')
    return ('/')

# Function to search and display Spotify tracks
def search_spotify():
    search_query = search_entry.get()
    headers = {'Authorization': f'Bearer {access_token}'}
    search_url = f'{SPOTIFY_API_URL}search?q={search_query}&type=track'
    response = requests.get(search_url, headers=headers)

    if response.status_code == 200:
        tracks = response.json().get('tracks', {}).get('items', [])
        result_text.delete(1.0, tk.END)  # Clear previous results

        for track in tracks:
            result_text.insert(tk.END, f"{track['name']} by {track['artists'][0]['name']}\n")
    else:
        messagebox.showerror('Error', 'Failed to fetch Spotify data. Please check your input or try again later.')

# Function to search and display YouTube videos
def search_youtube():
    query = search_entry.get()
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(q=query, part='snippet', type='video', maxResults=5)
    response = request.execute()

    result_text.delete(1.0, tk.END)  # Clear previous results

    for item in response['items']:
        title = item['snippet']['title']
        video_id = item['id']['videoId']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        result_text.insert(tk.END, f"{title}\n")
        result_text.insert(tk.END, f"   [Link]({video_url})\n\n")

# Create and place the widgets
auth_button = tk.Button(app, text='Authenticate with Spotify', command=authenticate)
auth_button.pack(pady=10)

search_label = ttk.Label(app, text='Search for tracks:')
search_label.pack()

search_entry = ttk.Entry(app, width=30)
search_entry.pack()

spotify_search_button = ttk.Button(app, text='Search on Spotify', command=search_spotify)
spotify_search_button.pack(pady=5)

youtube_search_button = ttk.Button(app, text='Search on YouTube', command=search_youtube)
youtube_search_button.pack(pady=5)

result_text = tk.Text(app, height=10, width=50)
result_text.pack()

app.mainloop()
