import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials


# Set up Spotipy API credentials
client_id = 'e3f2d17f8e3b4238bcc0b7075efbaf31'
client_secret = '9e014b9d45cf4295bbc57cd364ecb9df'


redirect_uri = 'http://127.0.0.1:5000'


# Initialize Spotipy API client with user authentication
scope = "playlist-modify-public"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

print(sp)

# Ask user for mood input
mood = input("What is your mood? ")

print(mood)

# Use Spotipy API to search for tracks based on the mood input
# sp.search(q='mood:' + mood, limit=50, offset=0, type='track')
results = sp.search(q='artist:' + 'Radiohead', type='artist')

items = results['artists']['items']
if len(items) > 0:
    artist = items[0]
    print(artist['name'], artist['images'][0]['url'])

# Create an empty list to store the track URIs
track_uris = []

# Extract track URIs from search results and add them to the list
for track in results['tracks']['items']:
    track_uris.append(track['uri'])

# Create a new private playlist with the given name and description
playlist_name = "My {} playlist".format(mood)
playlist_description = "A playlist for {} mood".format(mood)
playlist = sp.user_playlist_create(user=sp.current_user()['id'], name=playlist_name, public=False, description=playlist_description)

# Add the extracted track URIs to the newly created playlist
sp.playlist_add_items(playlist_id=playlist['id'], items=track_uris)

# Print success message
print("Playlist '{}' with {} tracks created successfully!".format(playlist_name, len(track_uris)))