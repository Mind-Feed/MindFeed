import tkinter as tk
from tkinter import messagebox
import webbrowser
from flask import Flask, request, redirect
import requests
import threading

app = Flask(__name__)

# Spotify API credentials
CLIENT_ID = '3dbfa5b09ce546448990687751ad470e'
CLIENT_SECRET = '142444ed089049a6bed24c4000c74708'
REDIRECT_URI = 'http://localhost:5000/callback'
SPOTIFY_API_URL = 'https://api.spotify.com/v1/'

# Variable to store the access token
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

# Route for the callback after successful authentication
@app.route('/callback')
def callback():
    global access_token  # Declare access_token as global variable
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
    tk.messagebox.showinfo('Authentication Successful', 'You have successfully authenticated with Spotify!')
    return redirect('/')

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
        tk.messagebox.showerror('Error', 'Failed to fetch Spotify data. Please check your input or try again later.')

# Create Tkinter window
root = tk.Tk()
root.title('Spotify Track Search')

# Authentication button
auth_button = tk.Button(root, text='Authenticate with Spotify', command=authenticate)
auth_button.pack(pady=10)

# Search input and button
search_label = tk.Label(root, text='Search for tracks:')
search_label.pack()

search_entry = tk.Entry(root, width=30)
search_entry.pack()

search_button = tk.Button(root, text='Search', command=search_spotify)
search_button.pack(pady=10)

# Results display
result_text = tk.Text(root, height=10, width=50)
result_text.pack()

# Run the Tkinter event loop
root.mainloop()
