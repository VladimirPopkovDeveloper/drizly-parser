# Using Standard requests.get
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import requests
import time

sitemap_path = "sitemapproducts.xml"
tree = ET.parse(sitemap_path)
root = tree.getroot()

links = []

# Iterate sitemap
for url in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
    link = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
    links.append(link)


max_attempts = 3  # Number of attempts
max_iterations = 5  # Number of iteration (for testing)

for i, link in enumerate(links):
    if i >= max_iterations:
        break  # Count iteration
    attempts = 0  # Count attempts
    while attempts < max_attempts:
        try:
            response = requests.get(link)
            if response.status_code == 200:
                break  # If server -> success
        except requests.exceptions.RequestException as e:
            print(f'Got unexpected exception: {repr(e)}')

        # If not, wait 5 sec
        time.sleep(5)
        attempts += 1

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
        
        print(f"Содержимое скрипта для ссылки {link} добавлено в файл scripts.json")
