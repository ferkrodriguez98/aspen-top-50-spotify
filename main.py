import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup # pip3 install BeuatifulSoup
from selenium import webdriver # pip3 install selenium
from selenium.webdriver.common.keys import Keys
import time
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

#url of the page we want to scrape
url = "https://www.radios-argentinas.org/fm-aspen-1023"

options = webdriver.ChromeOptions()

options.add_argument('--headless')

# initiating the webdriver. Parameter includes the path of the webdriver.
# acordate de instalar el driver !
driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=options)

f = open("tracks.txt", "r")

lines = f.read()
tracks = lines.splitlines()

f.close()

#####

while(True):

    driver.get(url)

    # this is just to ensure that the page is loaded
    time.sleep(5)

    html = driver.page_source

    # this renders the JS code and stores all
    # of the information in static HTML code.

    # Now, we could simply apply bs4 to html variable
    soup = BeautifulSoup(html, "html.parser")

    div_latest_song = soup.find('div', class_="latest-song")

    latest_song = div_latest_song.find('span', class_="song-name")
    latest_artist = div_latest_song.find('span', class_="artist-name")

    song_title = latest_song.find('p').text.strip()
    artist_name = latest_artist.text.strip()

    track_id = get_track_id(song_title, artist_name)

    if track_id != "None!":
        if len(tracks) != 0:
            if track_id != tracks[-1]: # aca tengo cuidado de no agregarlo dos veces seguidas
                tracks.append(track_id)
                with open('tracks.txt', 'a') as f:
                    f.write(track_id + '\n')
                    f.close()

        ordered_tracks = top_50(tracks) # funcion que agarre la lista tracks y me la devuelve ordenada por ocurrencias

        replace_playlist(ordered_tracks)

    time.sleep(120)