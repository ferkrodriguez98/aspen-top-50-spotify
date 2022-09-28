import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import Counter
from itertools import repeat, chain
import os
from pathlib import Path
import re
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

def get_song(url, chrome_service, chrome_options):
    #url of the page we want to scrape
    #url = "https://www.radios-argentinas.org/fm-aspen-1023"

    # initiating the webdriver.
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    driver.get(url)

    # this is just to ensure that the page is loaded
    time.sleep(5)

    html = driver.page_source

    driver.quit()

    # Now, we could simply apply bs4 to html variable
    soup = BeautifulSoup(html, "html.parser")

    div_latest_song = soup.find('div', class_="latest-song")

    latest_song = div_latest_song.find('span', class_="song-name")
    latest_artist = div_latest_song.find('span', class_="artist-name")

    song_title = latest_song.find('p').text.strip()
    artist_name = latest_artist.text.strip()

    song = song_title + " - " + artist_name

    return song, artist_name


def get_track_id(song):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth())
    
    song = re.sub("[\(\[].*?[\)\]]", "", song)

    track_search = sp.search(q=song, type='track', limit=1)

    if len(track_search['tracks']['items']) == 0:
        print("No results for song " + song)
        track_id = "None!"
    else:
        track_id = track_search['tracks']['items'][0]['uri']

    return track_id

def replace_playlist(tracks, playlist_id):
    scope = "playlist-modify-public"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    sp.playlist_replace_items(playlist_id, items=tracks)

    return None

def top_50(tracks):
    sorted_tracks = list(chain.from_iterable(repeat(i, c) for i,c in Counter(tracks).most_common()))

    removed_duplicates = list(dict.fromkeys(sorted_tracks))

    return removed_duplicates[0:50]

def get_lines_from_file(file):
    f = open(file, "r")

    lines = f.read()
    tracks = lines.splitlines()

    f.close()

    return tracks

def get_songs_only_past_week(file):
    tracks = get_lines_from_file(file)

    # now = datetime.now()
    # dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    if len(tracks) > 21000: # estimating 300 songs per day?
        tracks = tracks[-21000:]
    
    return tracks

def create_directory_if_not_exists(radio):
    PATH = './' + radio
    if not os.path.exists(PATH):
        os.makedirs(PATH)

    fle = Path('./' + radio + '/track_names.txt')
    fle.touch(exist_ok=True)
    f = open(fle)

    fle = Path('./' + radio + '/track_names_with_no_uri.txt')
    fle.touch(exist_ok=True)
    f = open(fle)

    fle = Path('./' + radio + '/tracks.txt')
    fle.touch(exist_ok=True)
    f = open(fle)

    fle = Path('./' + radio + '/possible_ads.txt')
    fle.touch(exist_ok=True)
    f = open(fle)

def write_track_to_files(song, track_id, radio, possible_ad):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    song = song + " // " + dt_string + " // " + track_id

    if possible_ad == False:
        if track_id != "None!":
            songs = get_lines_from_file(radio + "/track_names.txt")

            if len(songs) != 0:
                if song[0:5] != songs[-1][0:5]:
                    with open(radio + '/track_names.txt', 'a') as f:
                        print("Adding song to track_names.txt...")
                        f.write(song + '\n')
                        print("Number of songs scraped is: " + str(len(songs) + 1))
                        f.close()
            else:
                with open(radio + '/track_names.txt', 'a') as f:
                    print("Adding first song to track_names.txt...")
                    f.write(song + '\n')
                    f.close()

            tracks = get_lines_from_file(radio + "/tracks.txt")

            if len(tracks) != 0:
                if track_id != tracks[-1]: # aca tengo cuidado de no agregarlo dos veces seguidas
                    with open(radio + '/tracks.txt', 'a') as f:
                        print("Adding spotify uri to tracks.txt...")
                        f.write(track_id + '\n')
                        f.close()
            else:
                with open(radio + '/tracks.txt', 'a') as f:
                        print("Adding first spotify uri to tracks.txt...")
                        f.write(track_id + '\n')
                        f.close()

        else:
            print("Couldn't get track id :(")

            no_uri_songs = get_lines_from_file(radio + "/track_names_with_no_uri.txt")

            if len(no_uri_songs) != 0:
                if song[0:5] != no_uri_songs[-1][0:5]:
                    with open(radio + '/track_names_with_no_uri.txt', 'a') as f:
                        print("Adding song to track_names_with_no_uri.txt...")
                        f.write(song + '\n')
                        f.close()
            else:
                with open(radio + '/track_names_with_no_uri.txt', 'a') as f:
                        print("Adding first song to track_names_with_no_uri.txt...")
                        f.write(song + '\n')
                        f.close()
    else:
        with open(radio + '/possible_ads.txt', 'a') as f:
            print("Adding possible ad...")
            f.write(song + '\n')
            f.close()


def add_track(song, radio, possible_ad):
    # song = get_song(url, chrome_service, chrome_options)

    track_id = get_track_id(song)

    create_directory_if_not_exists(radio)

    print("------------------")
    print(radio)
    print(song)
    print(track_id)
    print("------------------")

    # forbidden songs
    
    # Chuck Buster: Earth 2 is terrible! - Patrick Marrinan // No tengo idea por que aparece tanto
    # Te Hacen Falta Vitaminas - Soda Stereo // Publicidad
    # Birds of Prey // Publicidad
    # Daycare - Huug // Ni idea man
    # Red States Blue States // Ni idea
    # Paisaje - Gilda // Publicidad
    # Easy Listening Jazz Background // Cortina?
    # Crumbs (feat. Blush'ko) - Jordan Dennis // Ni idea pero no esta bien en aspen esto asi que debe ser otra cosa
    # Late Night Show Intro (Live) - Kenny Fong // No se
    # 4 - Boca Junior Forever // Luquita Rodrigue
    # Battle Without Honor Or Humanity - Hotei // Kill Bill
    # Milonga de mis amores - Orquesta tipica de Pedro Laurenz // Ni idea
    # Sway with me // Ni idea
    # Joke's on you
    # In My Hood // Ni idea
    # tie break no se que
    # games timmy rickard
    # no estés triste buraq
    # arte - tango engrampado // no se por que suena en vorterix todos los dias a la media noche
    # stay de kid laroi y justin pero japonesa ? random
    # david guetta im good blue
    # i want it that way cantada por hijos de puta
    # once in a lifetime philip guyler
    # mi mami es mia ????
    # you be illin
    # angelito tu abuela
    # a danca das flores
    # balanda para un loco
    # querrequestyle

    forbidden_tracks = ["spotify:track:11iP5AN0ftQZbVU9SmFTrL", "spotify:track:3caBCFURBMGqZYrZUc7j8s", "spotify:track:7v1YbW8QYpfFebFmvhntrH", "spotify:track:44tv8coB9oOIVFmyCL7u1r", "spotify:track:4HgOxamRy4UXhCs5Bhw92J", "spotify:track:6NipZljiEekGRNF6vddEP3", "spotify:track:0Yeaq4bPZk7hcUrldSmASo", "spotify:track:0wgElszsos5fWd2lT8AJGG", "spotify:track:1joCD8lmeECxsuFllwWEgG", "spotify:track:4uB9aTwNWtrkfCkQh2dLoX", "spotify:track:6Q32Vkucx2qeuVyBd3NiFZ", "spotify:track:0DEa2fl4X6wPj1HFIF6y5o", "spotify:track:49BTcpVottyuoVxHQigMbP", "spotify:track:4l00HxpAXTr7O34ORXvSnK", "spotify:track:4QzTOliqElY3QcEQLG8zIk", "spotify:track:0PAaTyoLXpjGVe57EuuUed", "spotify:track:1efyjnQuyc7Lwj0FGQLC5a", "spotify:track:57ldajesvLV5Vnpri43bRh", "spotify:track:5DXZQV4VxXRllzwcZalTZL", "spotify:track:5fxyZf6m2xHeSrOzUfcJrq", "spotify:track:6prCjg1Aw78WViahkkxEXj", "spotify:track:218wqDZcPmIeSEEwBTZ2uP", "spotify:track:4N6wVUAMkVElse4sAHF0lF", "spotify:track:0cK8HYU0Mwaea9U1Ln56R5", "spotify:track:14423JlgVUbfpmQ9GRUGCu", "spotify:track:5m8WUAOtjHLt3y8UVPXUIm", "spotify:track:7pzdca5bXcVS8FvxEfy5HU", "spotify:track:0fCkqOUJ1J109Yu6TqJDq5", "spotify:track:4n35TddfNkMH1UnvfCgTkv", "spotify:track:67EuF0WdXxyv3fHb4zYFbB"]

    if track_id not in forbidden_tracks:
        write_track_to_files(song, track_id, radio, possible_ad)

    # write_track_to_files(song, track_id, radio, possible_ad)

def main(radio, url , chrome_service, chrome_options):
    song, artist_name = get_song(url, chrome_service, chrome_options)

    if artist_name not in ['Terry Devine-King', 'Timmy Rickard & James Stelling']: # xd
        add_track(song, radio, False)
