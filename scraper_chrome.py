# Using Chrone WebDriver (has problem with user profile, need fixes)
import xml.etree.ElementTree as ET
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


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

#options.add_argument('--user-data-dir=C:\\Users\\dj-ve\\AppData\\Local\\Google\\Chrome\\User Data')
#options.add_argument('--profile-directory=Default')

driver = webdriver.Chrome(options=options)

max_iterations = 30  # Number of iteration (for testing)

for i, link in enumerate(links):
    if i >= max_iterations:
        break  # Check iteration
    print(f"Открываем ссылку №: {i+1}")
    # Переход на страницу
    driver.get(link)

    # Ожидание CloudFlare и прочего дерьма
    try:
        # Ожидание появления кнопки "Подтвердить 21 год"
        submit_button_21years = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button.Yf9y6pN6bXzrDlVhFGb'))
        )

        # Автоматический клик по кнопке "Подтвердить 21 год"
        submit_button_21years.click()

        # Ожидание возможного окна captcha
        captcha_present = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.recaptcha'))
        )

        # Ожидание появления чекбокса "Я не робот"
        checkbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span.recaptcha-checkbox'))
        )

        # Автоматический клик по чекбоксу
        checkbox.click()

        # Ожидание исчезновения чекбокса "Я не робот"
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, 'span.recaptcha-checkbox'))
        )

        # Ожидание исчезновения окна CloudFlare
        WebDriverWait(driver, 30).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div#cf-splash-ovr'))
        )
    except:
        pass

    # Получение содержимого элемента
    try:
        script_content = driver.find_element("css selector", 'script[type="application/json"][data-hypernova-key="pdp_app_page"]').get_attribute('innerHTML').replace("<!--", "").replace("-->", "")
    except NoSuchElementException as exception:
        with open('badlinks.txt', 'a', encoding="utf-8") as f:
            f.write(link + '\n')
        print(f"Элемент не найден. Необработанная ссылка добавлена в badlinks.txt")

    # Вывод содержимого
    with open('scripts.json', 'a', encoding="utf-8") as f:
        f.write(script_content + '\n')
    print(f'Ссылка № {link.index(link)} {link} добавлена в файл scripts.json')

# Закрытие браузера
driver.quit()
