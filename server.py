import itertools
import random
import spotipy.util as util
from flask import Flask, redirect, request, jsonify
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

# client_id = 'e3f2d17f8e3b4238bcc0b7075efbaf31'
# client_secret = '9e014b9d45cf4295bbc57cd364ecb9df'

client_id = '03746619a3994ac7be5411d6a001355e'
client_secret = '97657b3eb1694e78b2d9693fe30447e6'



# ===============================================
# Initialize the Spotipy client with SpotifyOAuth
# ===============================================
def createToken():
        spotifyy = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri="http://127.0.0.1:5000",
                                               scope='user-library-read user-top-read playlist-modify-public user-follow-read user-read-private',
                                               cache_path=".spotifycache"))
        
        cached_token_info = spotifyy.auth_manager.get_cached_token()
        
        if cached_token_info:
            # If cached token info exists, return the access token and Spotify object
            return {"token": cached_token_info['access_token'], "spotify": spotifyy}
        else:
            # If cached token info does not exist, initiate the authorization flow and get the access token
            auth_url = spotifyy.auth_manager.get_authorize_url()
            print(f"Please go to this URL and authorize access: {auth_url}")
            response = input("Enter the URL you were redirected to: ")
            code = spotifyy.auth_manager.parse_response_code(response)
            token_info = spotifyy.auth_manager.get_access_token(code)
            spotifyy.auth_manager.cache_token(token_info)
            return {"token": token_info['access_token'], "spotify": spotifyy}


# Define list of moods
moods = ['happy', 'sad', 'energetic', 'relaxed', 'romantic', 'angry']

app = Flask(__name__)

# ====================================
# Get users mood and create a playlist
# ====================================
@app.route('/mood', methods=['POST'])
def mode():
    # image = request.get_json()["image"] 
    # predict_mood(image)
    # Get mood from request

    # token = util.prompt_for_user_token('Malith', 'user-library-read user-top-read playlist-modify-public user-follow-read user-read-private', client_id, client_secret, "http://127.0.0.1:5000")

    # if token:
    #     def authenticate_spotify():
    #         print("Authenticating Spotify...")
    #         sp = spotipy.Spotify(auth=token)
    #         return sp
        
    mood = request.get_json()["mood"] # happy
    response = createToken()
    # test_token = authenticate_spotify()
    accessToken = response["token"]
    spotifyy = response["spotify"]
    print(accessToken)
    print(spotifyy)

    #===========================================

    # Get user's and artists
    def top_artists_collection(spotifyy):
        print("Collecting Your Top artists for the last 6 months:")
        top_artists_name = []
        top_artists_uri = []

        ranges = ['short_term', 'medium_term']
        
        for range in ranges:
            top_artists_every_data = spotifyy.current_user_top_artists(limit=50, time_range=range)
            top_artists_data = top_artists_every_data['items']
            
            for data in top_artists_data:
                if data['name'] not in top_artists_name:
                    top_artists_name.append(data['name'])
                    top_artists_uri.append(data['uri'])

        # following_artists_every_data = spotifyy.current_user_followed_artists(limit=50)
        # print(following_artists_every_data)
        # following_artists_data = (following_artists_every_data['artists'])
        # #print(following_artists_data)
        
        # for data in following_artists_data['items']:
        #     if data['name'] not in top_artists_name:
        #         top_artists_name.append(data['name'])
        #         top_artists_uri.append(data['uri'])
        
    
        return top_artists_uri
    
    def top_tracks_collection(spotifyy, top_artists_uri):
        print("Collecting Your Top tracks for the last 6 months:")
        top_tracks_uri = []

        for artist in top_artists_uri:
            top_tracks_every_data = spotifyy.artist_top_tracks(artist)
            top_tracks_data = top_tracks_every_data['tracks']
            for track_data in top_tracks_data:
                top_tracks_uri.append(track_data['uri'])

        return top_tracks_uri
    

    
    
    def select_tracks_for_playlist(spotifyy, top_tracks_uri):
        print("Selecting tracks for playlist...")
        selected_tracks_uri = []

        def group(seq, size): 
         return (seq[pos:pos + size] for pos in range(0, len(seq), size))

        random.shuffle(top_tracks_uri)
        #for tracks in itertools.groupby(top_tracks_uri, lambda x: x // 50):
        for tracks in list(group(top_tracks_uri, 50)):
            audio_features = spotifyy.audio_features
            tracks_every_data = audio_features(tracks)

            # # Extract relevant audio features
            # valence = audio_features['valence']
            # energy = audio_features['energy']
            # danceability = audio_features['danceability']
            # instrumentalness = audio_features['instrumentalness']
            # liveness = audio_features['liveness']
            # mode = audio_features['mode']
            # loudness = audio_features['loudness']
            # speechiness = audio_features['speechiness']

            for track_data in tracks_every_data:

                try:
                    if (mood.lower() == "happy" 
                    and (0.7 < track_data["valence"] < 1.0)
                    and (0.7 < track_data["energy"] < 1.0)
                    and (0.7 < track_data["danceability"] < 1.0)
                    # and (0.0 < track_data["instrumentalness"] < 0.3)
                    # and (-8.0 < track_data["loudness"] < -5.0) 
                    # and (0.0 < track_data["speechiness"] < 0.3) 
                    # and (0.6 < track_data["liveness"] < 0.9) 
                    # and (track_data["mode"] == 1.0)
                    ):
                        selected_tracks_uri.append(track_data['uri'])
                    
                    elif (mood.lower() == "sad" 
                        and (0.0 < track_data["valence"] < 0.4) 
                        and (0.0 < track_data["energy"] < 0.4) 
                        and (0.0 < track_data["danceability"] < 0.4) 
                        # and 0.3 < track_data["instrumentalness"] < 0.8 \
                        # and -20.0 < track_data["loudness"] < -8.0 \
                        # and 0.0 < track_data["speechiness"] < 0.3 \
                        # and 0.0 < track_data["liveness"] < 0.4 \
                        # and 0.0 < track_data["mode"] < 0.4:
                        ):
                            selected_tracks_uri.append(track_data['uri'])

                    elif mood.lower == "angry" \
                        and 0.25 < track_data["valence"] < 0.35 \
                        and 0.7 < track_data["energy"] < 0.9 \
                        and 0.5 < track_data["danceability"] < 0.7 \
                        and 0.6 < track_data["instrumentalness"] < 0.8 \
                        and -8.0 < track_data["loudness"] < -5.0 \
                        and 0.2 < track_data["speechiness"] < 0.4 \
                        and 0.1 < track_data["liveness"] < 0.4 \
                        and 0.4 < track_data["mode"] < 0.6:
                            selected_tracks_uri.append(track_data['uri'])

                    elif mood.lower == "neutral" \
                        and 0.3 < track_data["valence"] < 0.5 \
                        and 0.3 < track_data["energy"] < 0.7 \
                        and 0.3 < track_data["danceability"] < 0.7 \
                        and 0.2 < track_data["instrumentalness"] < 0.6 \
                        and -15.0 < track_data["loudness"] < -8.0 \
                        and 0.2 < track_data["speechiness"] < 0.6 \
                        and 0.3 < track_data["liveness"] < 0.7 \
                        and 0.3 < track_data["mode"] < 0.7:
                            selected_tracks_uri.append(track_data['uri'])

                except TypeError as te:
                    continue

        return selected_tracks_uri
    
    def create_playlist(spotifyy, selected_tracks_uri):
        print("Creating playlist...")
    
        playlist_name = 'Playlist for ' + mood.lower() + ' mood'
        user_all_data = spotifyy.current_user()
        user_id = user_all_data['id']
        playlist = spotifyy.user_playlist_create(user=user_id, name=playlist_name)
        print(selected_tracks_uri)
        spotifyy.user_playlist_add_tracks(user=user_id, playlist_id=playlist['id'], tracks=selected_tracks_uri[0:30])
        print('hola2')
        playlist_url = playlist['external_urls']['spotify']
        print("Playlist created! Open it in Spotify with this link:")
        
        return playlist_url
        
    #===========================================

    #===========EXECUTION=================
    if mood.lower() in moods:
        top_artists_uri = top_artists_collection(spotifyy)
        top_tracks_uri = top_tracks_collection(spotifyy, top_artists_uri)
        selected_tracks_uri = select_tracks_for_playlist(spotifyy, top_tracks_uri)
        playlist_url = create_playlist(spotifyy, selected_tracks_uri)
        return jsonify({'result': playlist_url})

    else:
        print("Invalid mood. Please choose from happy, sad, energetic, relaxed, or romantic.")
        return jsonify({'result': "Invalid mood. Please choose from happy, sad, energetic, relaxed, or romantic."})


    # # Search for tracks based on mood
    # if mood.lower() in moods:
    #  results = spotifyy.search(q='genre:' + mood.lower(), limit=50, offset=0, type='track')
    #  tracks = results['tracks']['items']

    #     # Extract track IDs for each track
    #  track_ids = [track['id'] for track in tracks]
    
    #  # Create a new playlist on the user's account
    #  playlist_name = 'Playlist for ' + mood.lower() + ' mood'
    #  user_id = spotifyy.me()['id']
    #  playlist = spotifyy.user_playlist_create(user=user_id, name=playlist_name)
    
    #   # Add the tracks to the new playlist
    #  spotifyy.user_playlist_add_tracks(user=user_id, playlist_id=playlist['id'], tracks=track_ids)
    
    #  # Open the new playlist in the Spotify app
    #  playlist_url = playlist['external_urls']['spotify']
    #  print("Playlist created! Open it in Spotify with this link:")
    #  print(playlist_url)
    #  return jsonify({'result': playlist_url})
    
    # else:
    #     print("Invalid mood. Please choose from happy, sad, energetic, relaxed, or romantic.")
    #     return jsonify({'result': "Invalid mood. Please choose from happy, sad, energetic, relaxed, or romantic."})

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

def predict_mood(image):
    import cv2
    import tensorflow as tf
    import numpy as np
    import keras.utils as image
    import tensorflow_addons as tfa
    
    # Load the model
    with tf.keras.utils.custom_object_scope({'CohenKappa': tfa.metrics.CohenKappa(num_classes=4)}):
        model = tf.keras.models.load_model("C:/Users/malit/Downloads/my_trained_model3.h5")
    
    # Create a VideoCapture object to capture images from the camera
    # cap = cv2.VideoCapture(0)
    cap = image
    
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()
    
        # Display the frame
        cv2.imshow('frame', frame)
    
        # Wait for the user to press 'q' to quit or 'c' to capture a frame
        key = cv2.waitKey(1)
        if key == ord('q'):
        
            break
        elif key == ord('c'):
            # Convert the captured frame to a format that can be used by the model
            img = cv2.resize(frame, (300, 300))
            img = image.img_to_array(img)
            img = np.expand_dims(img, axis=0)
            img = img / 255.0  # normalize the pixel values
    
            # Classify the image using the trained model
            classes = model.predict(img, batch_size=10)[0]
            class_label = np.argmax(classes)
    
            # Map the class label to the corresponding class name
            if class_label == 0:
                print("Person is Happy")
                mood = "happy"
            elif class_label == 1:
                print("Person is Sad")
                mood = "happy"
            elif class_label == 2:
                print("Person is Angry")
                mood = "happy"
            else:
                print("Person is Neutral")
                mood = "happy"
    
    # Release the resources
    cap.release()
    cv2.destroyAllWindows()
    
