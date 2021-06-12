# -*- coding: utf8 -*-

#TODO
# - [] Coindar

# Импорт функций
from utils import *

# Другие либы
import sqlite3

# Либы для работы с телегой
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, user
from aiogram.dispatcher import FSMContext

#CONST
from config import botToken

#Описание команд
async def set_bot_commands(dp):
    commands = [
        types.BotCommand(command="price", description="[тикер монеты] — текущая цена"),
        types.BotCommand(command="change", description="[тикер монеты] — измененение цены монеты за 24 часа"),
        types.BotCommand(command="list", description="сводка о отслеживаемых монетах"),
        types.BotCommand(command="add", description="[тикер монеты] — добавить монету в список отслеживания"),
        types.BotCommand(command="remove", description="[тикер монеты] — удалить монету из списка отслеживания"),
        types.BotCommand(command="bubbles", description="визуализация рынка за неделю"),
        types.BotCommand(command="mood", description="настроение рынка на базе индикатора Bitcoin Rainbow Price Chart "),
        types.BotCommand(command="explorer", description="[адресс BTC кошелька] - информация о кошельке и QR код"),
        types.BotCommand(command="altindex", description="индекс сезона альткоинов"),
        types.BotCommand(command="fear", description="индекс страха и жадности"),
        types.BotCommand(command="help", description="справка по командам"),
        types.BotCommand(command="gas", description="цены на gas eth"),
        types.BotCommand(command="signal", description="[тикер монеты] [h/d/w/m] - результаты анализа рынка"),
        types.BotCommand(command="advsignal", description="[тикер монеты] [h/d/w/m] - продвинутые результаты анализа рынка"),
        types.BotCommand(command="profile", description="Список отслеживаемых монет и другая информация о профиле"),
    ]
    await dp.bot.set_my_commands(commands)

# Инициализация БД
connect = sqlite3.connect('coins.db')
cursor = connect.cursor()

# Инициализация бота
bot = Bot(token = botToken)
dp = Dispatcher(bot)

# Логика бота
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message, state: FSMContext):
    cursor.execute("""CREATE TABLE IF NOT EXISTS u{}(
        ticker TEXT
    )""".format(message.from_user.id))
    connect.commit()
    cursor.execute("SELECT * FROM u{}".format(message.from_user.id))
    coins = cursor.fetchall()
        
    await set_bot_commands(dp)
    await message.answer("Для получения справки по функциям бота использую /help \nСтраница проекта на GitHub - github.com/Forwall100/cryptanalyst_bot")


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
    if change24(coin) < 0:
        status = '📉 упал на '
    else:
        status = '📈 вырос на '

    await message.answer(coin + status + str(abs(round(change24(coin), 3))) + '%')


@dp.message_handler(commands="list")
async def send_list(message: types.Message):
    cursor.execute("SELECT * FROM u{}".format(message.from_user.id))
    coins = cursor.fetchall()
    await message.answer('Доминирование: ' + dominance())
    m = []
    await message.answer('⏳ Готовим актуальные данные...')
    for coin in coins:
        coin = coin[0]
        if change24(coin) < 0:
            status = '📉 упал на '
        else:
            status = '📈 вырос на '
        m.append('**{}**'.format(coin) + status + '`{}`'.format(str(round(abs(change24(coin)), 3)) + '%') + ' и теперь стоит ' + '`{}`'.format(str(price(coin)) + '$') + '\n' + sum_signals(coin)[0])
    for i in m:
        await message.answer(i, parse_mode='MarkdownV2')


@dp.message_handler(commands="add", content_types='text')
async def add_coin(message: types.Message):
    cursor.execute("SELECT * FROM u{}".format(message.from_user.id))
    coins = cursor.fetchall()
    if (message.text.replace('/add ', ''),) not in coins:
        cursor.execute("INSERT INTO u{} VALUES(?);".format(message.from_user.id), [message.text.replace('/add ', '')])
        connect.commit()
        await message.answer('Добавил тикер в список')
    else:
        await message.answer('Этот тикер уже есть в списке')
    

@dp.message_handler(commands="remove", content_types='text')
async def remove_coin(message: types.Message):
    cursor.execute("SELECT * FROM u{}".format(message.from_user.id))
    coins = cursor.fetchall()
    if (message.text.replace('/remove ', ''),) in coins:
        cursor.execute("DELETE FROM u{} WHERE ticker = ?".format(message.from_user.id), [message.text.replace('/remove ', '')])
        connect.commit()
        await message.answer('Удалил тикер из списка')
    else:
        await message.answer('Этого тикера нет в списке')


@dp.message_handler(commands="profile")
async def alt_answer(message: types.Message):
    cursor.execute("SELECT * FROM u{}".format(message.from_user.id))
    coins = cursor.fetchall()
    watching_coins = []
    for coin in coins:
        if coins.index(coin) + 1 == len(coins):
            watching_coins.append('└ `' + coin[0] + '`')
        else:
            watching_coins.append('├ `' + coin[0] + '`')
    await message.answer('🆔 Ваш ID: {}\n\n 🔎 Отслеживаемые монеты\n{}'.format('`{}`'.format(message.from_user.id), '\n'.join(watching_coins)), parse_mode='MarkdownV2')


@dp.message_handler(commands="mood", content_types='text')
async def mood_answer(message: types.Message):
    await message.answer(mood())

@dp.message_handler(commands='admin', content_types='text')
async def server_answer(message: types.Message):
    if message.from_user.id == admin_id:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        close = types.KeyboardButton(text="❌ Закрыть")
        statistic = types.KeyboardButton(text="📊 Статистика")
        keyboard.add(close, statistic)
        await message.answer('Вы вошли в админ панель', reply_markup=keyboard)
        @dp.message_handler(content_types='text')
        async def choise_answer(message: types.Message):
            if message.text == "📊 Статистика":
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                await message.answer('📊 Пользователей в боте - ' + str(len(cursor.fetchall())))
            if message.text == '❌ Закрыть':
                markup = types.ReplyKeyboardRemove()
                await message.answer('Вы вышли из админ панели', reply_markup=markup)
    else:
        await message.answer('Вы не администратор')


@dp.message_handler(commands="bubbles", content_types='text')
async def bubbles_answer(message: types.Message):
    await bot.send_photo(message.from_user.id, photo=open(bubble(), 'rb'))


@dp.message_handler(commands="fear", content_types='text')
async def mood_answer(message: types.Message):
    await message.answer(fear_and_greed_index()[0] + '\n ' + fear_and_greed_index()[1] + '\n ' + fear_and_greed_index()[2] + '\n ')


@dp.message_handler(commands="explorer", content_types='text')
async def explorer_answer(message: types.Message):
    address = message.text.replace('/explorer ', '')
    buttons = [
        types.InlineKeyboardButton(text="Blockchain", url="https://www.blockchain.com/ru/btc/address/"+address),
        types.InlineKeyboardButton(text="Intelx", url="https://intelx.io/?s="+address),
        types.InlineKeyboardButton(text="Whoiswho", url="https://bitcoinwhoswho.com/address/"+address)
    ]
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    await message.answer('⏳ Готовим актуальные данные')
    qr_code_url = btc_explorer(address)['qr_code_url']
    await message.answer('💎 Bitcoin адрес:\n' + '`{}`'.format(address) + '\n\n' + 'Транзакций: ' + '`{}`'.format(str(btc_explorer(address)['tx_count'])) + '\n' + 'Всего получено: ' + '`{} BTC`'.format(str(btc_explorer(address)['received'])) + '\n' + 'Всего отправлено: ' + '`{} BTC`'.format(str(btc_explorer(address)['sent'])) + '\n' + 'Итоговый баланс: ' + '`{}`'.format(str(btc_explorer(address)['balance'])), parse_mode='MarkdownV2', reply_markup=keyboard)
    await bot.send_photo(message.from_user.id, qr_code_url)


@dp.message_handler(commands="altindex", content_types='text')
async def alt_answer(message: types.Message):
    await message.answer('Индекс альтсезона сегодня - ' + alt_index() + '%')


@dp.message_handler(commands="gas")
async def alt_answer(message: types.Message):
    fast = gas()['FastGasPrice']
    propose = gas()['ProposeGasPrice']
    slow = gas()['SafeGasPrice']
    await message.answer('🚀 Быстро - ' + fast + ' gwei' + '\n👌Обычно - ' + propose + ' gwei ' + '\n🐢 Медленно - ' + slow + ' gwei ')


@dp.message_handler(commands="signal", content_types='text')
async def signal_answer(message: types.Message):
    ticker = message.text.replace('/signal ', '').split()[0]
    time = message.text.replace('/signal ', '').split()[1]
    await message.answer(sum_signals(ticker, time)[0] + ' по ' + ticker)
    await message.answer('Статистика по сигналам' + sum_signals(ticker, time)[1])


@dp.message_handler(commands="advsignal", content_types='text')
async def advsignal_answer(message: types.Message):
    ticker = message.text.replace('/advsignal ', '').split()[0]
    time = message.text.replace('/advsignal ', '').split()[1]
    await message.answer('Анализ по ' + ticker + '\n' + sum_signals_adv(ticker, time))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
