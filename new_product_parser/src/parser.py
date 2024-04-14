import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Access-Control-Request-Method': 'GET',
    'Access-Control-Request-Headers': 'x-queryid',
    'Referer': 'https://www.wildberries.ru/',
    'Origin': 'https://www.wildberries.ru',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
}

params = {
    'ab_testing': 'false',
    'appType': '1',
    'curr': 'rub',
    'dest': '-1257786',
    'query': 'игрушки для кошек',
    'resultset': 'catalog',
    'sort': 'popular',
    'spp': '30',
    'suppressSpellcheck': 'false',
}

response = requests.get('https://search.wb.ru/exactmatch/ru/common/v4/search', params=params, headers=headers)

print(response.status_code)
print(response.json())
