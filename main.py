from bs4 import BeautifulSoup # pip3 install BeuatifulSoup
from selenium import webdriver # pip3 install selenium
from selenium.webdriver.common.keys import Keys
import time
import functions
import chromedriver_autoinstaller

# this should run every 120 seconds

print("Starting...")

#url of the page we want to scrape
url = "https://www.radios-argentinas.org/fm-aspen-1023"

options = webdriver.ChromeOptions()

options.add_argument('--headless')
options.add_argument('--remote-debugging-port=9222')

# initiating the webdriver. Parameter includes the path of the webdriver.
driver = webdriver.Chrome(executable_path='./chromedriver', options=options)

tracks = functions.get_tracks_from_file()

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

track_id = functions.get_track_id(song_title, artist_name)

with open('track_names.txt', 'a') as f:
    print("Adding song to track_names.txt...")
    f.write(song_title + " - " + artist_name + '\n')
    f.close()

if track_id != "None!":
    if len(tracks) != 0:
        if track_id != tracks[-1]: # aca tengo cuidado de no agregarlo dos veces seguidas
            with open('tracks.txt', 'a') as f:
                print("Adding spotify uri to tracks.txt...")
                f.write(track_id + '\n')
                f.close()