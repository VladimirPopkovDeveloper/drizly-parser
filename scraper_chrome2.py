from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#create chromeoptions instance
options = webdriver.ChromeOptions()

options.add_argument("start-maximized") # open Browser in maximized mode
options.add_argument("disable-infobars") # disabling infobars
options.add_argument("--disable-extensions") # disabling extensions
options.add_argument("--disable-gpu") # applicable to windows os only
options.add_argument("--disable-dev-shm-usage") # overcome limited resource problems

options.add_argument("--no-sandbox") # Bypass OS security model

#provide location where chrome stores profiles
options.add_argument(r"--user-data-dir=C:\\Users\\dj-ve\\AppData\\Local\\Google\\Chrome\\User Data")

#provide the profile name with which we want to open browser
options.add_argument(r'--profile-directory=Profile 4')

#specify where your chrome driver present in your pc
driver = webdriver.Chrome(options=options)

#provide website url here
driver.get("https:#drizly.com/liquor/tequila/blanco-silver/avion-silver-tequila/p3833")

