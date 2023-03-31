import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id = 'e3f2d17f8e3b4238bcc0b7075efbaf31'
client_secret = '9e014b9d45cf4295bbc57cd364ecb9df'

# Create a SpotifyOAuth object with cache_path specified
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri="http://127.0.0.1:5000/setToken",
                                               scope='user-library-read playlist-modify-public user-read-private', cache_path=".spotifycache"))

# Call the sp.current_user() method to test if authentication is successful
results = sp.playlist_tracks('4mo6dTF2o2I3PChPoKnEUg')
print(results)