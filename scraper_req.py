# Using Standard requests + scraping from Google cashe (might be blocked, but has some prospects)
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import requests
import time
import random

sitemap_path = "sitemapproducts.xml"
tree = ET.parse(sitemap_path)
root = tree.getroot()
# Add cookies
cookies = {
    'forterToken': 'e1c8bbce1a0f4f9ba2bf2c6191c2e986_1683363672186_897_UAL9_6',
}
# Add headers
headers = {
    'authority': 'webcache.googleusercontent.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ka;q=0.6,bg;q=0.5',
    'cache-control': 'no-cache',
    # 'cookie': 'forterToken=e1c8bbce1a0f4f9ba2bf2c6191c2e986_1683363672186_897_UAL9_6',
    'pragma': 'no-cache',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"112.0.5615.139"',
    'sec-ch-ua-full-version-list': '"Chromium";v="112.0.5615.139", "Google Chrome";v="112.0.5615.139", "Not:A-Brand";v="99.0.0.0"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-ch-ua-wow64': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'x-client-data': 'CI62yQEIorbJAQjEtskBCKmdygEI14jLAQiSocsBCOyezQEI9p/NAQiFoM0BCL2izQEIn6TNAQjQpc0BCNemzQEI3KbNAQiHp80BCJCqzQEIparNAQjfq80BCM+uzQE=',
}

links = []

# Iterate sitemap
for url in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
    link = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
    links.append(link)

print(f"Ссылки из sitemapproducts.xml загружены")

max_attempts = 3  # Number of attempts
max_iterations = 30  # Number of iteration (for testing)

for i, link in enumerate(links):
    if i >= max_iterations:
        break  # Check iteration
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
        print(f'Ответ сервера: {response.status_code}')
        time.sleep(random.randint(5, 20))  # Wait some random time
        attempts += 1
        print(f'Попытка №: {attempts}')

    if attempts == max_attempts:
        print(f"Не удалось получить ответ от сервера для ссылки: {link}")
        
        # Save bad link to file
        with open('badlinks.txt', 'a', encoding="utf-8") as f:
            f.write(link + '\n')
        print(f"Необработанная ссылка добавлена в badlinks.txt")
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
        time.sleep(random.randint(5, 20)) # Wait some random time
