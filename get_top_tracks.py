import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-top-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# Knock On Wood - Amii Stewart

tracks = sp.current_user_top_tracks(time_range="short_term")

for idx, item in enumerate(tracks['items']):
    print(item["name"] + " - " + item["album"]["name"])