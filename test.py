# primero te paras en la carpeta y haces python3 -m venv env
# despues source env/bin/activate
# despues los pip3 install

from bs4 import BeautifulSoup # pip3 install BeuatifulSoup
from selenium import webdriver # pip3 install selenium
from selenium.webdriver.common.keys import Keys
import time
  
#url of the page we want to scrape
url = "https://www.radios-argentinas.org/fm-aspen-1023"
  
# initiating the webdriver. Parameter includes the path of the webdriver.
driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
driver.get(url)
  
# this is just to ensure that the page is loaded
time.sleep(5)
  
html = driver.page_source
  
# this renders the JS code and stores all
# of the information in static HTML code.

# Now, we could simply apply bs4 to html variable
soup = BeautifulSoup(html, "html.parser")

# es un span con class np__info_principal

song = soup.find('div', class_="latest-song")

print(song)
