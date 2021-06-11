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

from requests.sessions import session

#CONST
from config import *

#Функции
def get_id(ticker):
    with open('get_id.json', 'r') as file:
        data = json.load(file)
        for coin in data:
            if coin['symbol'] == ticker or coin['symbol'] == ticker.lower():
                return coin['id']


def change24(ticker):
    id = get_id(ticker)
    url = 'https://api.coingecko.com/api/v3/simple/price?ids={}&vs_currencies=usd&include_24hr_change=true'.format(id)
    try:
        r = requests.get(url)
        data = r.json()
        return data[id]['usd_24h_change']
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e


def price(ticker):
    id = get_id(ticker)
    url = 'https://api.coingecko.com/api/v3/simple/price?ids={}&vs_currencies=usd'.format(id)
    try:
        r = requests.get(url)
        data = r.json()
        return data[id]['usd']
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e


def name(ticker):
    id = get_id(ticker)
    url = 'https://api.coingecko.com/api/v3/coins/{}'.format(id)
    try:
        r = requests.get(url)
        data = r.json()
        return data['name']
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
    for i in m:
        try:
            i.remove('Extreme')
        except:
            pass
    return [('Сегодня ' + translate(m[0][-2]) + ' ' + m[0][-1]), ('Вчера ' + translate(m[1][-2]) + ' ' +  m[1][-1]), ('Прошлая неделя ' + translate(m[-2][2]) + ' ' +  m[2][-1])]


def btc_explorer(address):
    url = 'https://bitcoinwhoswho.com/address/' + address
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    qr_code_url = soup.find_all('img', attrs={'alt':'QR Code'})[0]['src']

    url = 'https://chain.api.btc.com/v3/address/' + address
    data = requests.get(url).json()['data']
    received = data['received']/100000000
    sent = data['sent']/100000000
    balance = data['balance']
    tx_count = data['tx_count']
    return {'qr_code_url':qr_code_url, 'received':str(received) + ' = ~' + str(round(price('BTC') * received, 2)) + '$', 'sent':str(sent) + ' = ~' + str(round(price('BTC') * received, 2)) + '$', 'balance':balance, 'tx_count':tx_count}


def alt_index():
    url = 'https://www.blockchaincenter.net/altcoin-season-index/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    m = []
    for child in soup.find_all('div', attrs={"class":"bccblock"}):
        m.append(child.text.replace('\n', '').replace('%', ''))
    return m[1][22:24]


def gas():
    url = 'https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey='+ethscan
    session = Session()
    try:
        response = session.get(url)
        data = json.loads(response.text)
        return data['result']
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e


def trand(ticker, time='d'):
    # Определение периода торговли
    if time == 'h':
        period = '17'
    elif time == 'd':
        period = '30'
    elif time == 'w':
        period = '50'
    elif time == 'm':
        period = '70'

    url = 'https://api.taapi.io/ema?secret={}&exchange=binance&symbol={}/USDT&interval=1{}&optInTimePeriod={}'.format(taapiTocken, ticker, time, period)
    session = Session()
    try:
        response = session.get(url)
        data = json.loads(response.text)
        if data['value'] >= price(ticker):
            return 'bear'
        else:
            return 'bull'
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e


def rsi(ticker, time='d'):
    url = 'https://api.taapi.io/rsi?secret={}&exchange=binance&symbol={}/USDT&interval=1{}'.format(taapiTocken, ticker, time)
    session = Session()
    try:
        response = session.get(url)
        data = json.loads(response.text)
        if data['value'] > 70:
            return 'bear'
        elif data['value'] < 30:
            return 'bull'
        else:
            return 'neutral'
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e


def bbands(ticker, time='d'):
    url = 'https://api.taapi.io/bbands2?secret={}&exchange=binance&symbol={}/USDT&interval=1{}'.format(taapiTocken, ticker, time)
    session = Session()
    try:
        response = session.get(url)
        data = json.loads(response.text)
        if price(ticker) > data['valueUpperBand']:
            return 'bear'
        elif price(ticker) < data['valueLowerBand']:
            return 'bull'
        else:
            return 'neutral'
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e


def macd(ticker, time='d'):
    url = 'https://api.taapi.io/macd?secret={}&exchange=binance&symbol={}/USDT&interval=1{}'.format(taapiTocken, ticker, time)
    session = Session()
    try:
        response = session.get(url)
        data = json.loads(response.text)
        if abs(data['valueMACD']) < abs(data['valueMACDSignal']):
            return 'bear'
        elif abs(data['valueMACD']) > abs(data['valueMACDSignal']):
            return 'bull'
        else:
            return 'neutral'
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e


def stochrs(ticker, time='d'):
    url = 'https://api.taapi.io/stochrsi?secret={}&exchange=binance&symbol={}/USDT&interval=1{}'.format(taapiTocken, ticker, time)
    session = Session()
    try:
        response = session.get(url)
        data = json.loads(response.text)
        if data['valueFastK'] > 80:
            return 'bear'
        elif data['valueFastK'] < 20:
            return 'bull'
        else:
            return 'neutral'
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e


def ishimoku(ticker, time='d'):
    url = 'https://api.taapi.io/ichimoku?secret={}&exchange=binance&symbol={}/USDT&interval=1{}&backtracks=10'.format(taapiTocken, ticker, time)
    session = Session()
    try:
        response = session.get(url)
        data = json.loads(response.text)
        m = []
        for i in data:
            del i['conversion'], i['base'], i['spanA'], i['spanB'], i['laggingSpanA'], i['laggingSpanB']
            m.append(i['currentSpanA']-i['currentSpanB'])
        s = []
        for i in m:
            s.append(abs(i))
        if m[s.index(min(s))] > 0:
            return 'bear'
        elif m[s.index(min(s))] < 0:
            return 'bull'
        else:
            return 'neutral'
    except:
        pass


def sum_signals(ticker, time='d'):
    m = []
    try:
        m.append(trand(ticker, time))
    except:
        pass
    try:
        m.append(rsi(ticker))
    except:
        pass
    try:
        m.append(bbands(ticker))
    except:
        pass
    try:
        m.append(macd(ticker))
    except:
        pass
    try:
        m.append(stochrs(ticker))
    except:
        pass
    try:
        m.append(ishimoku(ticker))
    except:
        pass

    if ticker != 'BTC' and int(alt_index()) >= 75:
        m.append('bull')
    elif ticker != 'BTC' and int(alt_index()) <= 25:
        m.append('bear')
    elif ticker == 'BTC' and int(alt_index()) >= 75:
        m.append('bear')
    elif ticker == 'BTC' and int(alt_index()) <= 25:
        m.append('bull')
    else:
        m.append('neutral')

    if int(fear_and_greed_index()[0].split()[-1]) < 50:
        m.append('bull')
    elif int(fear_and_greed_index()[0].split()[-1]) > 50:
        m.append('bear')
    else:
        m.append('neutral')

    res = []
    bull = m.count('bull')
    bear = m.count('bear')
    neutral = m.count('neutral')
    if bull > bear and bull > neutral:
        res.append('🐂 Бычий прогноз') 
    elif bear > bull and bear > neutral:
        res.append('🐻 Медвежий прогноз') 
    else:
        res.append('🙈 Нейтральный прогноз')

    res.append('\n🐻 Медвежьи: ' + str(bear) + '\n🐂 Бычьи: ' + str(bull) + '\n🙈 Нейтральные: ' + str(neutral))
    return res


def sum_signals_adv(ticker, time='d'):
    m = []
    try:
        m.append((trand(ticker, time), 'EMA'))
    except:
        pass
    try:
        m.append((rsi(ticker), 'RSI'))
    except:
        pass
    try:
        m.append((bbands(ticker), 'Bollinger Bands'))
    except:
        pass
    try:
        m.append((macd(ticker), 'MACD'))
    except:
        pass
    try:
        m.append((stochrs(ticker), 'Stochastic Relative Strength'))
    except:
        pass
    try:
        m.append((ishimoku(ticker), 'Ichimoku Cloud'))
    except:
        pass

    if ticker != 'BTC' and int(alt_index()) >= 75:
        m.append(('bull', 'Altcoin Seson'))
    elif ticker != 'BTC' and int(alt_index()) <= 25:
        m.append(('bear', 'Altcoin Seson'))
    elif ticker == 'BTC' and int(alt_index()) >= 75:
        m.append(('bear', 'Altcoin Seson'))
    elif ticker == 'BTC' and int(alt_index()) <= 25:
        m.append(('bull', 'Altcoin Seson'))
    else:
        m.append(('neutral', 'Altcoin Seson'))

    if int(fear_and_greed_index()[0].split()[-1]) < 50:
        m.append(('bull', 'Fear and Greed'))
    elif int(fear_and_greed_index()[0].split()[-1]) > 50:
        m.append(('bear', 'Fear and Greed'))
    else:
        m.append(('neutral', 'Fear and Greed'))
    bull = []
    bear = []
    neutral = []
    res_bear = []
    res_bull = []
    res_neutral = []
    for i in m:
        if i[0] == 'bear':
            bear.append(i[1])
        elif i[0] == 'bull':
            bull.append(i[1])
        elif i[0] == 'neutral':
            neutral.append(i[1])

    res_bear.append('🐻 Медвежьи: ' + str(len(bear)) + ' - ')
    for i in bear:
        res_bear.append(i + ', ')

    res_bull.append('🐂 Бычьи: ' + str(len(bull)) + ' - ')
    for i in bull:
        res_bull.append(i + ', ')

    res_neutral.append('🙈 Нейтральные: ' + str(len(neutral)) + ' - ')
    for i in neutral:
        res_neutral.append(i + ', ')
    
    return ''.join(res_bear) + '\n' + ''.join(res_bull) + '\n' + ''.join(res_neutral)