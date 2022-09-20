import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-top-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

tracks = sp.current_user_top_tracks(time_range="long_term")

for idx, item in enumerate(tracks['items']):
    print(item["name"] + " - " + item["album"]["name"])

artists = sp.current_user_top_artists(time_range="long_term")

for idx, item in enumerate(artists['items']):
    print(item["name"])