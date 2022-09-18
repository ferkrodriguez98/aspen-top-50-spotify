import time
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

track_id = functions.get_track_id(song_title, artist_name)

with open('track_names.txt', 'a') as f:
    print("Adding song to track_names.txt...")
    f.write(song_title + " - " + artist_name + '\n')
    f.close()

tracks = functions.get_tracks_from_file()

if track_id != "None!":
    if len(tracks) != 0:
        if track_id != tracks[-1]: # aca tengo cuidado de no agregarlo dos veces seguidas
            with open('tracks.txt', 'a') as f:
                print("Adding spotify uri to tracks.txt...")
                f.write(track_id + '\n')
                f.close()