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
print("------------------")

chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

# funcion que le pegue a la url y devuelva un track id

def get_song(radio, url):

    #url of the page we want to scrape
    #url = "https://www.radios-argentinas.org/fm-aspen-1023"

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

    print("------------------")
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

    song = song_title + " - " + artist_name

    track_id = functions.get_track_id(song)

    # forbidden songs (?)
    # Chuck Buster: Earth 2 is terrible! - Patrick Marrinan
    # Te Hacen Falta Vitaminas - Soda Stereo

    print("------------------")
    print(radio)
    print(song)
    print(track_id)
    print("------------------")

    functions.create_directory_if_not_exists(radio)

    # forbidden songs
    # Chuck Buster: Earth 2 is terrible! - Patrick Marrinan // No tengo idea por que aparece tanto
    # Te Hacen Falta Vitaminas - Soda Stereo // Publicidad
    # Birds of Prey // Publicidad
    # Daycare - Huug // Ni idea man
    # Red States Blue States // Ni idea
    # Paisaje - Gilda // Publicidad
    # Easy Listening Jazz Background // Cortina?

    forbidden_tracks = ["spotify:track:11iP5AN0ftQZbVU9SmFTrL", "spotify:track:3caBCFURBMGqZYrZUc7j8s", "spotify:track:7v1YbW8QYpfFebFmvhntrH", "spotify:track:44tv8coB9oOIVFmyCL7u1r", "spotify:track:4HgOxamRy4UXhCs5Bhw92J", "spotify:track:6NipZljiEekGRNF6vddEP3", "spotify:track:0Yeaq4bPZk7hcUrldSmASo"]

    if track_id not in forbidden_tracks:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        song = song + " // " + dt_string + " // " + track_id
        functions.write_track_to_files(song, track_id, radio)

    driver.quit()

get_song("aspen", "https://www.radios-argentinas.org/fm-aspen-1023")
get_song("vorterix", "https://www.radios-argentinas.org/radio-vorterix")
get_song("rock&pop", "https://www.radios-argentinas.org/radio-rock-and-pop")
get_song("blue", "https://www.radios-argentinas.org/radio-blue")
get_song("mega", "https://www.radios-argentinas.org/mega-983")
