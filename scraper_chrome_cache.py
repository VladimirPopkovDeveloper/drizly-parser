# Using Chrone WebDriver (has problem with user profile, need fixes)
import xml.etree.ElementTree as ET
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Get sitemap
sitemap_path = "sitemapproducts.xml"
tree = ET.parse(sitemap_path)
root = tree.getroot()

links = []

# Iterate sitemap
for url in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
    link = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
    links.append(link)

print(f"Ссылки из sitemapproducts.xml загружены")

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")  # Опция для уменьшения вероятности появления защиты CloudFlare
options.add_argument("--disable-extensions")
options.add_argument('--no-sandbox')
#options.add_argument('--user-data-dir=C:\\Users\\dj-ve\\AppData\\Local\\Google\\Chrome\\User Data')
#options.add_argument('--profile-directory=Default')

driver = webdriver.Chrome(options=options)

max_iterations = 20  # Number of iteration (for testing)

for i, link in enumerate(links):
    if i >= max_iterations:
        break  # Check iteration
    print(f"Открываем ссылку №: {i+1}")
    # Переход на страницу
    driver.get('https://webcache.googleusercontent.com/search?q=cache:'+link)
        
    # Ожидание появления кнопки "Подтвердить 21 год"
    try:
        yes_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='YES']")))
        yes_button.click()
    except:
        pass

    # Получение содержимого элемента
    try:
        script_content = driver.find_element("css selector", 'script[type="application/json"][data-hypernova-key="pdp_app_page"]').get_attribute('innerHTML').replace("<!--", "").replace("-->", "")
    except:
        with open('parser_log.txt', 'a', encoding="utf-8") as f:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f'{i} - {timestamp} - не добавлена - {link} \n')

    # Вывод содержимого
    with open('scripts.json', 'a', encoding="utf-8") as f:
        f.write(script_content + '\n')
    with open('parser_log.txt', 'a', encoding="utf-8") as f:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'{i} - {timestamp} - {link} \n')
    print(f'Ссылка {link} добавлена в файл scripts.json')
    time.sleep(random.randint(2, 10)) # Wait some random time

# Закрытие браузера
driver.quit()
