from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#create chromeoptions instance
options = webdriver.ChromeOptions()

#provide location where chrome stores profiles
options.add_argument(r"--user-data-dir=C:\\Users\\dj-ve\\AppData\\Local\\Google\\Chrome\\User Data")

#provide the profile name with which we want to open browser
options.add_argument(r'--profile-directory=Default')

#specify where your chrome driver present in your pc
driver = webdriver.Chrome(options=options)

#provide website url here
driver.get("https://drizly.com/liquor/tequila/blanco-silver/avion-silver-tequila/p3833")

