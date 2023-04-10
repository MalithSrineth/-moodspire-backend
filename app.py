
import random
from flask import Flask, redirect, request, jsonify
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cv2
import tensorflow as tf
import numpy as np
import keras.utils as image
import tensorflow_addons as tfa
from flask import Flask
from flask_cors import CORS



client_id = 'e3f2d17f8e3b4238bcc0b7075efbaf31'
client_secret = '9e014b9d45cf4295bbc57cd364ecb9df'

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


# Load the models
# with tf.keras.utils.custom_object_scope({'CohenKappa': tfa.metrics.CohenKappa(num_classes=4)}):
#     model = tf.keras.models.load_model("my_trained_model3.h5")

model = tf.keras.models.load_model("my_trained_model3.h5")

def predict_mood(imagee):
    
    # img = cv2.resize(image, (300, 300))

    # Read the image file
    image = cv2.imdecode(np.frombuffer(imagee.read(), np.uint8), cv2.IMREAD_COLOR)

    # Resize the image to (224, 224)dir
    image = cv2.resize(image, (300, 300), interpolation=cv2.INTER_AREA)

    # Convert the image to a numpy array
    image = np.asarray(image, dtype=np.float32).reshape(300, 300, 3)

    # image = image.img_to_array(image)
    image = np.expand_dims(image, axis=0)

    # Normalize the image
    image = (image / 255.0)


    # Classify the image using the trained model
    classes = model.predict(image)[0]

    class_label = np.argmax(classes)

    # Map the class label to the corresponding class name
    if class_label == 0:
        print("Person is Happy")
        mood = "happy"
        return mood
    elif class_label == 1:
        print("Person is Sad")
        mood = "sad"
        return mood
    elif class_label == 2:
        print("Person is Angry")
        mood = "angry"
        return mood
    else:
        print("Person is Neutral")
        mood = "neutral"
        return mood
    

# Define list of moods
moods = ['happy', 'sad', 'neutral', 'angry']

app = Flask(__name__)

# ====================================
# Get users mood and create a playlist
# ====================================
@app.route('/mood', methods=['POST'])
def mode():
    image = request.files["image"]
    mood = predict_mood(image)

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
        for tracks in list(group(top_tracks_uri, 50)):
            audio_features = spotifyy.audio_features
            tracks_every_data = audio_features(tracks)

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

                    elif (mood.lower == "angry"
                        and (0.25 < track_data["valence"] < 0.35)
                        or (0.7 < track_data["energy"] < 0.9)
                        or (0.5 < track_data["danceability"] < 0.7) 
                        # and 0.6 < track_data["instrumentalness"] < 0.8 \
                        # and -8.0 < track_data["loudness"] < -5.0 \
                        # and 0.2 < track_data["speechiness"] < 0.4 \
                        # and 0.1 < track_data["liveness"] < 0.4 \
                        # and 0.4 < track_data["mode"] < 0.6:
                        ):
                            selected_tracks_uri.append(track_data['uri'])

                    elif (mood.lower == "neutral"
                        and (0.3 < track_data["valence"] < 0.5) 
                        and (0.3 < track_data["energy"] < 0.7) 
                        and (0.3 < track_data["danceability"] < 0.7) 
                        # and 0.2 < track_data["instrumentalness"] < 0.6 \
                        # and -15.0 < track_data["loudness"] < -8.0 \
                        # and 0.2 < track_data["speechiness"] < 0.6 \
                        # and 0.3 < track_data["liveness"] < 0.7 \
                        # and 0.3 < track_data["mode"] < 0.7:
                    ):
                            selected_tracks_uri.append(track_data['uri'])

                except TypeError as te:
                    continue
                    
        return selected_tracks_uri
    
    def create_playlist(spotifyy, selected_tracks_uri):
        playlist_name = 'Playlist for ' + mood.lower() + ' mood'
        user_all_data = spotifyy.current_user()
        user_id = user_all_data['id']
        playlist = spotifyy.user_playlist_create(user=user_id, name=playlist_name)
        
        spotifyy.user_playlist_add_tracks(user=user_id, playlist_id=playlist['id'], tracks=selected_tracks_uri[0:30])
        playlist_url = playlist['external_urls']['spotify']
        print("Playlist created! Open it in Spotify with this link:")
        
        # print(playlist['uri'])
        return playlist['uri']
        
    #===========================================

    #===========EXECUTION=================
    if mood.lower() in moods:
        top_artists_uri = top_artists_collection(spotifyy)
        top_tracks_uri = top_tracks_collection(spotifyy, top_artists_uri)
        selected_tracks_uri = select_tracks_for_playlist(spotifyy, top_tracks_uri)
        playlist_uri = create_playlist(spotifyy, selected_tracks_uri)
        return jsonify({'result': playlist_uri})

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
    CORS(app)
    app.run()



    
