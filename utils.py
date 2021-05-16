# Другие либы
import sqlite3

# Сетевые либы
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import hashlib

#CONST
from config import coinMarketCapToken
from config import screenshotapiToken

#Функции
def change24(asset):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol': asset
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': coinMarketCapToken,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data['data'][asset]['quote']['USD']['percent_change_24h']
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e

def price(asset):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol': asset
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': coinMarketCapToken,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data['data'][asset]['quote']['USD']['price']
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e

def name(asset):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol': asset
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': coinMarketCapToken,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data['data'][asset]['name']
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e

def dominance():
    url = 'https://coinmarketcap.com/ru/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    return(soup.find_all('a', attrs={'href':'/ru/charts/#dominance-percentage'})[0].text)

def mood():
    url = 'https://www.blockchaincenter.net/bitcoin-rainbow-chart/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    legend = soup.find_all('div', attrs={'class':'legend'})
    for child in soup.recursiveChildGenerator():
        if child.name == 'span':
            if len(child.attrs['class']) == 2:
                if child.text == 'Maximum Bubble Territory':
                    return 'Максимальный пузырь'
                elif child.text == 'Sell. Seriously, SELL!':
                    return 'Продавайте. Серьезно, ПРОДАВАЙТЕ!'
                elif child.text == 'FOMO intensifies':
                    return 'Фома усиливается'
                elif child.text == 'Is this a bubble?':
                    return 'Это пузырь?'
                elif child.text == 'HODL!':
                    return 'HODL!'
                elif child.text == 'Still cheap':
                    return 'Все еще дешево'
                elif child.text == 'Accumulate':
                    return 'Накапливаем'
                elif child.text == 'BUY!':
                    return 'ПОКУПАЕМ!'
                elif child.text == 'Basically a Fire Sale':
                    return 'Огненная распродажа'

def generate_screenshot_api_url(customer_key, secret_phrase, options):
    api_url = 'https://api.screenshotmachine.com/?key=' + customer_key
    if secret_phrase:
        api_url = api_url + '&hash=' + hashlib.md5((options.get('url') + secret_phrase).encode('utf-8')).hexdigest()
    api_url = api_url + '&' + urllib.parse.urlencode(options)
    return api_url

def bubble():
    customer_key = screenshotapiToken
    secret_phrase = ''
    options = {
    'url': 'https://cryptobubbles.net',
    'dimension': '1366x768', 
    'device': 'desktop',
    'format': 'jpg',
    'cacheLimit' : '0',
    'delay' : '4000',
    'zoom' : '100',
    'click': '#CloseCoinzillaHeader'
    }
    url = generate_screenshot_api_url(customer_key, secret_phrase, options)
    file = open('./bubbles.jpg', 'wb')
    file.write(requests.get(url).content)
    file.close()
    return './bubbles.jpg'

def fear_and_greed_index():
    def translate(x):
        if x == 'Fear':
            return 'страх 😱'
        elif x == 'Greed':
            return 'жадность 🤑'
    url = 'https://alternative.me/crypto/fear-and-greed-index/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    m = []
    historical = soup.find_all('div', attrs={'class':'fng-value'})
    for i in historical:
        if i.text != '':
            m.append(i.text.replace('\n', ' ').split())
    return [('Сегодня ' + translate(m[0][-2]) + ' ' + m[0][-1]), ('Вчера ' + translate(m[1][-2]) + ' ' +  m[1][-1]), ('Прошлая неделя ' + translate(m[-2][2]) + ' ' +  m[2][-1])]

def btc_explorer(address):
    url = 'https://live.blockcypher.com/btc/address/' + address
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    m = []
    for i in soup.find_all('li'):
        if 'RECEIVED' or 'SENT' or 'BALANCE' in i.text:
            m.append(i.text.replace('\n', ' '))
    return [m[-1], m[-2], m[-3], 'https:' + soup.find_all('img')[0]['src']]

def alt_index():
    url = 'https://www.blockchaincenter.net/altcoin-season-index/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    m = []
    for child in soup.find_all('div', attrs={"class":"bccblock"}):
        m.append(child.text.replace('\n', '').replace('%', ''))
    return m[1][22:24]
    