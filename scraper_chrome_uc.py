# Using Chrome UC (has problem with user profile, need fixes, but avoid fucking CloudFlare)
import xml.etree.ElementTree as ET
import undetected_chromedriver as uc
import datetime
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

options = uc.ChromeOptions()
options.add_argument("--start-maximized")
#options.add_argument('--user-data-dir=C:\\Users\\dj-ve\\AppData\\Local\\Google\\Chrome\\User Data')
#options.add_argument('--profile-directory=Default')

driver = uc.Chrome(options=options)

start_element = 30000 # Start from this element in Link array
end_element = 50000  # Finish on this element in Link array

for i, link in enumerate(links[start_element:], start_element): # Start from this element in Link array
    if i >= end_element: # Proceed by end element
        break  # Check iteration
    print(f"Открываем ссылку №: {i+1}")
    # Переход на страницу
    driver.get(link)
        
    # Получение содержимого элемента
    try:
        script_content = driver.find_element("css selector", 'script[type="application/json"][data-hypernova-key="pdp_app_page"]').get_attribute('innerHTML').replace("<!--", "").replace("-->", "")
    except:
        with open('parser_log.txt', 'a', encoding="utf-8") as f:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f'{i} - {timestamp} - не добавлена - {link} \n')

    # Вывод содержимого
    with open('scripts3.json', 'a', encoding="utf-8") as f:
        f.write(script_content + '\n')
    with open('parser_log3.txt', 'a', encoding="utf-8") as f:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'{i} - {timestamp} - {link} \n')
    print(f'Ссылка {link} добавлена в файл scripts3.json')
    time.sleep(random.randint(2, 10)) # Wait some random time

# Закрытие браузера
driver.quit()
