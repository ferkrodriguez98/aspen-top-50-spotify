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

# lo que deberia hacer es ir a buscar la cancion, guardarme el nombre, esperar 10 segundos, buscarla de vuelta. si el nombre coincide entonces no es propaganda?

functions.main("aspen", "https://www.radios-argentinas.org/fm-aspen-1023", chrome_service, chrome_options)
functions.main("vorterix", "https://www.radios-argentinas.org/radio-vorterix", chrome_service, chrome_options)
functions.main("rock&pop", "https://www.radios-argentinas.org/radio-rock-and-pop", chrome_service, chrome_options)
functions.main("blue", "https://www.radios-argentinas.org/radio-blue", chrome_service, chrome_options)
functions.main("mega", "https://www.radios-argentinas.org/mega-983", chrome_service, chrome_options)
