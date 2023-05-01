# Using Standard requests + scraping from Google cashe (might be blocked, but has some prospects)
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import requests
import time
import random

sitemap_path = "sitemapproducts.xml"
tree = ET.parse(sitemap_path)
root = tree.getroot()

links = []

# Iterate sitemap
for url in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
    link = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
    links.append(link)

print(f"Ссылки загружены")

max_attempts = 3  # Number of attempts
max_iterations = 50000  # Number of iteration (for testing)

for i, link in enumerate(links):
    if i >= max_iterations:
        break  # Count iteration
    print(f"Читаем ссылку №: {i+1}")
    attempts = 0  # Count attempts
    while attempts < max_attempts:
        try:
            cache_url = 'https://webcache.googleusercontent.com/search?q=cache:'+link
            response = requests.get(cache_url)
            if response.status_code == 200:
                break  # If server -> success
        except requests.exceptions.RequestException as e:
            print(f'Got unexpected exception: {repr(e)}')

        # If not:
        print(f'Server status code: {response.status_code}')
        time.sleep(random.randint(10, 30))  # Wait some random time
        attempts += 1
        print(f'Attempt #: {attempts}')

    if attempts == max_attempts:
        print(f"Не удалось получить ответ от сервера для ссылки: {link}")
    else:
        # If success -> continue
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')
        script_tag = soup.find('script', {'data-hypernova-key': 'pdp_app_page'})
        script_content = script_tag.string.replace("<!--", "").replace("-->", "")
        
        # Save script content to file
        with open('scripts.json', 'a', encoding="utf-8") as f:
            f.write(script_content + '\n')
        
        print(f"Содержимое скрипта # {i+1} для ссылки {link} добавлено в файл scripts.json")
        time.sleep(random.randint(10, 30)) # Wait some random time
