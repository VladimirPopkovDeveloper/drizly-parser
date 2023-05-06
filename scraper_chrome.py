# Using Chrone WebDriver (has problem with user profile, need fixes)
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
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")  # Опция для уменьшения вероятности появления защиты CloudFlare

#options.add_argument('--user-data-dir=C:\\Users\\dj-ve\\AppData\\Local\\Google\\Chrome\\User Data')
#options.add_argument('--profile-directory=Default')

driver = webdriver.Chrome(options=options)

for url in urls:
    # Переход на страницу
    driver.get(url)
    driver.add_cookie({"name":"ad_uuid", "value": "web%3A7a6be866-177a-4b14-9d3e-f7736ac8cd99"})
    driver.add_cookie({"name":"ab_uuid", "value": "490deeea-eebb-4fa4-8d70-1f1fcc32903d"})
    driver.add_cookie({"name":"_gcl_au", "value": "1.1.368385469.1680872502"})
    driver.add_cookie({"name":"ftr_ncd", "value": "6"})
    driver.add_cookie({"name":"_uetvid", "value": "5f235e80d54411ed821799b75777c702"})
    driver.add_cookie({"name":"has_address", "value": "false"})
    driver.add_cookie({"name":"referrer", "value": "https%3A%2F%2Fwebcache.googleusercontent.com%2F"})
    driver.add_cookie({"name":"__cf_bm", "value": "hDCoBXRPYY1WsXGSjSSNgwODdM17uR34bAQ_gCrHTgs-1683368529-0-AQ0BH7zGKQsCs0Mw7+sn9UREKf7D3SOEjnKWyrUMR6QI5dxuELmn7Imwen9IfrScmJuWzpTkip+DmuLm62IAIGoIuWFrr4LZRvCYXurrJhW5Sfmvx6qcT14zVcPaC62xhQ=="})
    driver.add_cookie({"name":"_drizly_web_session", "value": "UFFCT0UwU3hCaXgyajJXZGFEUkRCT2JBZlRLREtKWDBKbDlNNitHcEZHWThGM2NQOTlvNmZ3d1pFQURNOUYzbWFoMG1yTEZaMWlCbU96WENVNCtiN0lNZ2FEdW5qbEJOYUFVcEowU21RbEtna3BoZk0zQ0tRdXROYkVhaGtLVXZVSWNuOWpxb2FReXpFY042UFQ4YlhtNHM1Nkk5MmhBU2thR3pnamJDNXN5S3FtRitCcXpNaGZSSWlkOFROR3B2V3dGZGFzVThxdkdZWTZlZi8yNlZhRHdhRmlBa1JxYnNwdUh3eUkyTStFc3F0OVRETUZxdTZrMmFSZHA1ZDg5WnVoRllpSk4zT1Axem4xaVM5MGtaY1VENnpwclc0N1IyV0FiQWRYejNaVDdKZTlVWmJkRFZ1Z1o3bktOYjUzcFNTK3ZFbnBsRGNzVGx0OGpZYzVOY2FiTVFlck1jZWZTUHh6ZHVzTzNSeTNzTkYzUzR6S0N0VEFuQzUvUHQ3QlNqT2hKNG1LNHNXUGUwQ01hdnQwRjMvL3R6dUVsUmVUZ1A3UmVvamtqa1V5T1R5Z1gwWVQvTjRKbmU1Z28wbnlRdC81dGJIV0k3QThtWmRxRXJMdEtmYTNyMWlKOFVBMkRYek9vcVVFK0ZqaVM0YUFuY1AxWnVyQ005LzFybXNVQnZkV3BCK1p6NXcvaC9NOTVJNHJxU2FRdVlrTi9YZmY0cW9uek1oS0pWTnRwMXhVMEpua0huMnZpeTZaZnJqa2l2Sks1c0ZlcHFQVi9qRDRZb25CNmxqQktBUEZBWkw3NHIrVnlYVUdKVWpIUmI1aEdJZ21KdDlmQ3dtR1p3bGt6b2pUUnYwQ2lrRjJ4MUFuS21GSzZVNVdzRmg4d1BqMkdzaGtXa21LeVFPbTY0bzF6VmhQSTk1QlBjbWpzVlBhVE1NeDhLL3pRZHJpTTI2cWFMS1N0NnltNWE5TjBialUxeGd0NTYxeUhZcWY5Z1BiRFQ3VWkvN0N1OEF4N200TGN0YjVkMnVmYk1oZkwvOEFzSFNBREw0clQrNjA4ejJwcnQxeTZMSEdKOE1KejhQM09OR1g1dm5JczZhYXhMazNSdnNBc1Z4NjJXdFRkL3pMZ3gxWGl0Sm10eXlLanZTenp5L3QxK2cvMmNpa1lSSDcwVHJsbUdMVlRWNW01bnQ2WlN2N0cyeFQ0R3NBaFVnbFp4UjUxeHYyR1BDUC9qaURkMTB0TGVVSUJrdWpJUS9mUEJWNXlOVDgvK2hGcGlZODltMEd5a3JSVStSVEZEVXNvWG9vQXFRTjZ2K29PWllDbG9WMWQva2tncXp2RytRVlJDckIzZUdPUlpXM2s0SGRKWGNkbHRXM2pzRGppQXZXN3dnODA2RVpNTkhLUDNrV3p6eGk0TXBYdUtYWUsvNGNOeWRXenlBa1JFRFgrZ0tNcklMUGhLWkMvMFdFL29TR0FxbGdlTzY0N3JOZFprSEFOOGlHRkpnRHgwbnk1NnJUeEQzTlNSZkVadHZGaDE0bmVTLS1nT3pKaVlJUVVFMTNyNHF6RWZkWnFRPT0%3D--2b0e5e9b71b94c2fdea3fa75887d157b779e1eee"})
    driver.add_cookie({"name":"forterToken", "value": "18b8fbbcc9e6419ca9596e185f9fc0ec_1683364751848_850_UAL9_6"})

    # Ожидание CloudFlare

    try:
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

        # Ожидание появления кнопки "Подтвердить 21 год"
        submit_button_21years = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button.Yf9y6pN6bXzrDlVhFGb'))
        )

        # Автоматический клик по кнопке "Подтвердить 21 год"
        submit_button_21years.click()

        # Ожидание исчезновения окна CloudFlare
        WebDriverWait(driver, 30).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, 'div#cf-splash-ovr'))
        )

    except:
        pass

    # Получение содержимого элемента
    try:
        script_content = driver.find_element("css selector", 'script[type="application/json"][data-hypernova-key="pdp_app_page"]').get_attribute('innerHTML').replace("<!--", "").replace("-->", "")
    except:
        pass

    # Вывод содержимого
    print(script_content)
    with open('scripts.json', 'a', encoding="utf-8") as f:
        f.write(script_content + '\n')

# Закрытие браузера
driver.quit()
