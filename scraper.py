import xml.etree.ElementTree as ET
from scrapingant_client import ScrapingAntClient, ScrapingantClientException, ScrapingantInvalidInputException
from bs4 import BeautifulSoup
import time

client = ScrapingAntClient(token='e95b043e4a614c79ac7a0ef47757d8c9')

sitemap_path = "sitemapproducts.xml"
tree = ET.parse(sitemap_path)
root = tree.getroot()

links = []

# Итерируемся по всем элементам `url` в sitemap и добавляем значение `loc` в список ссылок
for url in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
    link = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
    links.append(link)


max_attempts = 3  # Максимальное количество попыток
max_iterations = 5  # Максимальное количество итераций цикла for

for i, link in enumerate(links):
    if i >= max_iterations:
        break  # Если количество итераций превышает 10, выходим из цикла
    attempts = 0  # Счетчик попыток
    while attempts < max_attempts:
        try:
            response = client.general_request(link)
            if response.status_code == 200:
                break  # Если сервер вернул успешный ответ, выходим из цикла
        except ScrapingantInvalidInputException as e:
            print(f'Got invalid input exception: {{repr(e)}}')
            break  # We are not retrying if request params are not valid
        except ScrapingantClientException as e:
            print(f'Got ScrapingAnt exception {repr(e)}')
        except Exception as e:
            print(f"Got unexpected exception: {repr(e)}")

        # Если сервер не ответил успешно, ждем 5 секунд перед повторной попыткой
        time.sleep(5)
        attempts += 1

    if attempts == max_attempts:
        print(f"Не удалось получить ответ от сервера для ссылки: {link}")
    else:
        # Если сервер вернул успешный ответ, продолжаем выполнение кода
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')
        script_tag = soup.find('script', {'data-hypernova-key': 'pdp_app_page'})
        script_content = script_tag.string.replace("<!--", "").replace("-->", "")
        
        # Сохраняем содержимое скрипта в файл в режиме дополнения
        with open('scripts.json', 'a', encoding="utf-8") as f:
            f.write(script_content + '\n')
        
        print(f"Содержимое скрипта для ссылки {link} добавлено в файл scripts.json")