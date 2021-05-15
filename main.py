# -*- coding: utf8 -*-

# Другие либы
import sqlite3
import shutil

# Сетевые либы
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import hashlib

# Либы для работы с телегой
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

#CONST
from config import coinMarketCapToken
from config import botToken
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
    return [('Сегодня ' + translate(m[0][1]) + ' ' + m[0][2]), ('Вчера ' + translate(m[1][1]) + ' ' +  m[1][2]), ('Прошлая неделя ' + translate(m[2][2]) + ' ' +  m[2][3])]

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

# Инициализация БД
connect = sqlite3.connect('coins.db')
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS coins(
    ticker TEXT
)""")
connect.commit()
cursor.execute("SELECT * FROM coins")
coins = cursor.fetchall()

# Логика бота
bot = Bot(token = botToken)
dp = Dispatcher(bot)

@dp.message_handler(commands="help")
async def send_help(message: types.Message):
    await message.answer('/price [тикер монеты] — текущая цена \n /change [тикер монеты] — измененение цены монеты за 24 часа \n /list — сводка о отслеживаемых монетах \n /add [тикер монеты] — добавить монету в список отслеживания \n /remove [тикер монеты] — удалить монету из списка отслеживания \n /bubbles - Визуализация рынка за неделю \n /mood - настроение рынка на базе индикатора Bitcoin Rainbow Price Chart \n /explorer [адресс BTC кошелька] - информация о кошельке и QR код \n /altindex - Индекс сезона альткоинов \n /fearAndGreed - Индекс страха и жадности')

@dp.message_handler(commands="price", content_types='text')
async def send_price(message: types.Message):
    coin = message.text.replace('/price ', '')
    await message.answer(coin + ' стоит ' + str(round(price(coin), 4)) + '$')

@dp.message_handler(commands="change", content_types='text')
async def send_change(message: types.Message):
    coin = message.text.replace('/change ', '')
    if change24(coin[0]) < 0:
        status = '📉 упал на '
    else:
        status = '📈 вырос на '

    await message.answer(coin[0] + status + str(abs(round(change24(coin[0]), 3))) + '%')

@dp.message_handler(commands="list")
async def send_list(message: types.Message):
    cursor.execute("SELECT * FROM coins")
    coins = cursor.fetchall()
    await message.answer('Доминирование: ' + dominance())
    for coin in coins:
        coin = coin[0]
        if change24(coin) < 0:
            status = '📉 упал на '
        else:
            status = '📈 вырос на '
        await message.answer(coin + status + str(abs(round(change24(coin), 3))) + '% и теперь стоит ' + str(round(price(coin), 4)) + '$')

@dp.message_handler(commands="add", content_types='text')
async def add_coin(message: types.Message):
    cursor.execute("SELECT * FROM coins")
    coins = cursor.fetchall()

    if (message.text.replace('/add ', ''),) not in coins:
        cursor.execute("INSERT INTO coins VALUES(?);", [message.text.replace('/add ', '')])
        connect.commit()
        await message.answer('Добавил тикер в список')
    else:
        await message.answer('Этот тикер уже есть в списке')
    

@dp.message_handler(commands="remove", content_types='text')
async def remove_coin(message: types.Message):
    cursor.execute("SELECT * FROM coins")
    coins = cursor.fetchall()

    if (message.text.replace('/remove ', ''),) in coins:
        cursor.execute(f"DELETE FROM coins WHERE ticker = ?", [message.text.replace('/remove ', '')])
        connect.commit()
        await message.answer('Удалил тикер из списка')
    else:
        await message.answer('Этого тикера нет в списке')

@dp.message_handler(commands="mood", content_types='text')
async def mood_answer(message: types.Message):
    await message.answer(mood())

@dp.message_handler(commands="bubbles", content_types='text')
async def bubbles_answer(message: types.Message):
    await bot.send_photo(message.from_user.id, photo=open(bubble(), 'rb'))

@dp.message_handler(commands="fearAndGreed", content_types='text')
async def mood_answer(message: types.Message):
    await message.answer(fear_and_greed_index()[0] + '\n ' + fear_and_greed_index()[1] + '\n ' + fear_and_greed_index()[2] + '\n ')

@dp.message_handler(commands="explorer", content_types='text')
async def explorer_answer(message: types.Message):
    await message.answer((btc_explorer(message.text.replace('/explorer ', ''))[0] + btc_explorer(message.text.replace('/explorer ', ''))[1] + btc_explorer(message.text.replace('/explorer ', ''))[2]).replace('Balance', 'Баланс').replace('Sent', 'Отправлено').replace('Received', 'Получено'))
    await bot.send_photo(message.from_user.id, btc_explorer(message.text.replace('/explorer ', ''))[3])

@dp.message_handler(commands="altindex", content_types='text')
async def alt_answer(message: types.Message):
    await message.answer('Индекс альтсезона сегодня - ' + alt_index() + '%')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)