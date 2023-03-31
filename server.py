from flask import Flask, redirect, request, jsonify
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

client_id = 'e3f2d17f8e3b4238bcc0b7075efbaf31'
client_secret = '9e014b9d45cf4295bbc57cd364ecb9df'

# ===============================================
# Initialize the Spotipy client with SpotifyOAuth
# ===============================================
def createToken():
        spotifyy = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri="www.google.com",
                                               scope='user-library-read playlist-modify-public user-read-private',
                                               cache_path=".spotifycache"))
        
        cached_token_info = spotifyy.auth_manager.get_cached_token()
        return {"token":cached_token_info['access_token'], "spotify":spotifyy}


# Define list of moods
moods = ['happy', 'sad', 'energetic', 'relaxed', 'romantic']

app = Flask(__name__)

# ====================================
# Get users mood and create a playlist
# ====================================
@app.route('/mood', methods=['POST'])
def mode():
    # Get mood from request
    mood = request.get_json()["mood"] # happy
    response = createToken()
    accessToken = response["token"]
    spotifyy = response["spotify"]
    print(accessToken)
    print(spotifyy)


    # Search for tracks based on mood
    if mood.lower() in moods:
     results = spotifyy.search(q='genre:' + mood.lower(), limit=50, offset=0, type='track')
     tracks = results['tracks']['items']

        # Extract track IDs for each track
     track_ids = [track['id'] for track in tracks]
    
     # Create a new playlist on the user's account
     playlist_name = 'Playlist for ' + mood.lower() + ' mood'
     user_id = spotifyy.me()['id']
     playlist = spotifyy.user_playlist_create(user=user_id, name=playlist_name)
    
      # Add the tracks to the new playlist
     spotifyy.user_playlist_add_tracks(user=user_id, playlist_id=playlist['id'], tracks=track_ids)
    
     # Open the new playlist in the Spotify app
     playlist_url = playlist['external_urls']['spotify']
     print("Playlist created! Open it in Spotify with this link:")
     print(playlist_url)
     return jsonify({'result': playlist_url})
    
    else:
        print("Invalid mood. Please choose from happy, sad, energetic, relaxed, or romantic.")
        return jsonify({'result': "Invalid mood. Please choose from happy, sad, energetic, relaxed, or romantic."})

# ===================
# Sample POST request
# ===================
@app.route('/post-example', methods=['POST'])
def post_example():
    # Get the data from the request
    data = request.get_json()
    print(data)
    # Do something with the data
    result = data['message']
    # Return the result as JSON
    return jsonify({'result': result})


# ============
# Server Start
# ============
if __name__ == '__main__':
    app.run()

