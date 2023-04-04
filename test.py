import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import requests
import json



# Ask user for mood input
mood = input("What is your mood? ")
headers = {'Content-Type': 'application/json'}
response = requests.request("POST", 'http://localhost:5000/mood', headers=headers, data=json.dumps({'mood': mood}))
print(response.json())

