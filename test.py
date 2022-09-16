# primero te paras en la carpeta y haces python3 -m venv env
# despues source env/bin/activate
# despues los pip3 install

from bs4 import BeautifulSoup # pip3 install BeuatifulSoup
from selenium import webdriver # pip3 install selenium
from selenium.webdriver.common.keys import Keys
import time
  
#url of the page we want to scrape
url = "https://www.radios-argentinas.org/fm-aspen-1023"

options = webdriver.ChromeOptions()

options.add_argument('--headless')

# initiating the webdriver. Parameter includes the path of the webdriver.
# acordate de instalar el driver !
driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=options)

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

print(song_title + " - " + artist_name)