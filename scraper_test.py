import requests
from bs4 import BeautifulSoup

cookies = {
    'forterToken': 'e1c8bbce1a0f4f9ba2bf2c6191c2e986_1683363672186_897_UAL9_6',
}

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

response = requests.get(
    'https://webcache.googleusercontent.com/search?q=cache:https://drizly.com/beer/ale/ipa/avery-hazyish-ipa/p92286',
    cookies=cookies,
    headers=headers,
)

html_content = response.content
soup = BeautifulSoup(html_content, 'html.parser')
script_tag = soup.find('script', {'data-hypernova-key': 'pdp_app_page'})
script_content = script_tag.string.replace("<!--", "").replace("-->", "")

print(script_content)