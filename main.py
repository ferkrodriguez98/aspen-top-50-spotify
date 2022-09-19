#!/bin/bash -l

import time
from datetime import datetime
import functions
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# this should run every 120 seconds

print("Starting...")

chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

#url of the page we want to scrape
url = "https://www.radios-argentinas.org/fm-aspen-1023"

chrome_options = Options()

options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]

for option in options:
    chrome_options.add_argument(option)

# initiating the webdriver.
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

#

print("Getting page source...")

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

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

song = song_title + " - " + artist_name + " // " + dt_string

track_id = functions.get_track_id(song_title, artist_name)

print(song)
print(track_id)

if track_id != "None!":
    songs = functions.get_lines_from_file("track_names.txt")

    if len(songs) != 0:
        if song[0:5] != songs[-1][0:5]:
            with open('track_names.txt', 'a') as f:
                print("Adding song to track_names.txt...")
                f.write(song + '\n')
                f.close()
    else:
        with open('track_names.txt', 'a') as f:
            print("Adding first song to track_names.txt...")
            f.write(song + '\n')
            f.close()

    tracks = functions.get_lines_from_file("tracks.txt")

    if len(tracks) != 0:
        if track_id != tracks[-1]: # aca tengo cuidado de no agregarlo dos veces seguidas
            with open('tracks.txt', 'a') as f:
                print("Adding spotify uri to tracks.txt...")
                f.write(track_id + '\n')
                f.close()
    else:
        with open('tracks.txt', 'a') as f:
                print("Adding first spotify uri to tracks.txt...")
                f.write(track_id + '\n')
                f.close()

else:
    print("Couldn't get track id :(")

    no_uri_songs = functions.get_lines_from_file("track_names_with_no_uri.txt")

    if len(no_uri_songs) != 0:
        if song[0:5] != no_uri_songs[-1][0:5]:
            with open('track_names_with_no_uri.txt', 'a') as f:
                print("Adding song to track_names_with_no_uri.txt...")
                f.write(song + '\n')
                f.close()
    else:
        with open('track_names_with_no_uri.txt', 'a') as f:
                print("Adding first song to track_names_with_no_uri.txt...")
                f.write(song + '\n')
                f.close()