# Using ScrapingAntClient Libs (too slow...)
import xml.etree.ElementTree as ET
from scrapingant_client import ScrapingAntClient, ScrapingantClientException, ScrapingantInvalidInputException
from bs4 import BeautifulSoup
import time

client = ScrapingAntClient(token='e95b043e4a614c79ac7a0ef47757d8c9')

sitemap_path = "sitemapproducts.xml"
tree = ET.parse(sitemap_path)
root = tree.getroot()

links = []

# Iterate sitemap
for url in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
    link = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
    links.append(link)


max_attempts = 3  # Number of attempts
max_iterations = 30  # Number of iteration (for testing)

for i, link in enumerate(links):
    if i >= max_iterations:
        break  # Count iteration
    attempts = 0  # Count attempts
    while attempts < max_attempts:
        try:
            cache_url = 'https://webcache.googleusercontent.com/search?q=cache:'+link
            response = client.general_request(cache_url)
            if response.status_code == 200:
                break  # If server -> success
        except ScrapingantInvalidInputException as e:
            print(f'Got invalid input exception: {{repr(e)}}')
            break  # We are not retrying if request params are not valid
        except ScrapingantClientException as e:
            print(f'Got ScrapingAnt exception {repr(e)}')
        except Exception as e:
            print(f"Got unexpected exception: {repr(e)}")

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