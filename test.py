import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import requests
import json

# client_id = 'e3f2d17f8e3b4238bcc0b7075efbaf31'
# client_secret = '9e014b9d45cf4295bbc57cd364ecb9df'

# Define list of moods
# moods = ['happy', 'sad', 'energetic', 'relaxed', 'romantic']

# Ask user for mood input
mood = input("What is your mood? ")
headers = {'Content-Type': 'application/json'}
response = requests.request("POST", 'http://localhost:5000/mood', headers=headers, data=json.dumps({'mood': mood}))
print(response.json())

# spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id,
#                                                client_secret=client_secret))

# # Initialize the Spotipy client with SpotifyOAuth
# spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
#                                                client_secret=client_secret,
#                                                redirect_uri="http://127.0.0.1:5000",
#                                                scope='user-library-read playlist-modify-public user-read-private'))

# # Search for tracks based on mood
# if mood.lower() in moods:
#     results = spotify.search(q='genre:' + mood.lower(), limit=50, offset=0, type='track')
#     tracks = results['tracks']['items']

#     # Extract track IDs for each track
#     track_ids = [track['id'] for track in tracks]
    
#     # Create a new playlist on the user's account
#     playlist_name = 'Playlist for ' + mood.lower() + ' mood'
#     user_id = spotify.me()['id']
#     playlist = spotify.user_playlist_create(user=user_id, name=playlist_name)
    
#     # Add the tracks to the new playlist
#     spotify.user_playlist_add_tracks(user=user_id, playlist_id=playlist['id'], tracks=track_ids)
    
#     # Open the new playlist in the Spotify app
#     playlist_url = playlist['external_urls']['spotify']
#     print("Playlist created! Open it in Spotify with this link:")
#     print(playlist_url)
    
# else:
#     print("Invalid mood. Please choose from happy, sad, energetic, relaxed, or romantic.")