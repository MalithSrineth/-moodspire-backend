import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = 'e3f2d17f8e3b4238bcc0b7075efbaf31'
client_secret = '9e014b9d45cf4295bbc57cd364ecb9df'

# Ask user for mood input
mood = input("What is your mood? ")

birdy_uri = 'spotify:mood:' + mood
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id,
                                               client_secret=client_secret))

results = spotify.search(q='mood:' + mood, limit=50, offset=0, type='track')

print(results)

albums = results['items']