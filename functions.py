import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter
from itertools import repeat, chain
import sys

def get_track_id(track, artist):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth())
    track = sp.search(q='artist:' + artist + ' track:' + track, type='track', limit=1)

    if len(track['tracks']['items']) == 0:
        track_id = "None!"

    track_id = track['tracks']['items'][0]['uri']

    return track_id

def replace_playlist(tracks):
    scope = "playlist-modify-public"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    playlist_id = '7bZVSBqJalnab6Yl6bGk3a' # constante

    sp.playlist_replace_items(playlist_id, items=tracks)

    return None

def top_50(tracks):
    sorted_tracks = list(chain.from_iterable(repeat(i, c) for i,c in Counter(tracks).most_common()))

    removed_duplicates = list(set(sorted_tracks))

    return removed_duplicates[0:50]

def get_tracks_from_file():
    f = open("tracks.txt", "r")

    lines = f.read()
    tracks = lines.splitlines()

    f.close()

    return tracks