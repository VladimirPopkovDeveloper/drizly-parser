from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

urls = [
    "https://drizly.com/wine/white-wine/sauvignon-blanc/cloudy-bay-sauvignon-blanc/p2734",
    "https://drizly.com/liquor/whiskey/bourbon/wild-turkey-101/p1552",
    "https://drizly.com/liquor/tequila/blanco-silver/avion-silver-tequila/p3833"
]

options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=C:\\Users\\dj-ve\\AppData\\Local\\Google\\Chrome\\User Data')
options.add_argument('--profile-directory=Default')

driver = webdriver.Chrome(options=options)

for url in urls:
    # Переход на страницу
    driver.get(url)

    try:
        # Ожидание возможного окна captcha
        captcha_present = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.recaptcha'))
        )
        print("Captcha detected. Please solve manually and then press enter to continue.")
        input()
    except:
        pass

    # Получение содержимого элемента
    script_content = driver.find_element("css selector", 'script[type="application/json"][data-hypernova-key="pdp_app_page"]').get_attribute('innerHTML').replace("<!--", "").replace("-->", "")

    # Вывод содержимого
    print(script_content)

# Закрытие браузера
driver.quit()
