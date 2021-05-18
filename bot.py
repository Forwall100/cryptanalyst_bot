# -*- coding: utf8 -*-

# Импорт функций
from utils import *

# Другие либы
import sqlite3

# Либы для работы с телегой
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
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
        types.BotCommand(command="help", description="справка по командам")
    ]
    await dp.bot.set_my_commands(commands)

# Инициализация БД
connect = sqlite3.connect('coins.db')
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS coins(
    ticker TEXT
)""")
connect.commit()
cursor.execute("SELECT * FROM coins")
coins = cursor.fetchall()

# Инициализация бота

bot = Bot(token = botToken)
dp = Dispatcher(bot)

# Логика бота

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message, state: FSMContext):
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


@dp.message_handler(commands="fear", content_types='text')
async def mood_answer(message: types.Message):
    await message.answer(fear_and_greed_index()[0] + '\n ' + fear_and_greed_index()[1] + '\n ' + fear_and_greed_index()[2] + '\n ')


@dp.message_handler(commands="explorer", content_types='text')
async def explorer_answer(message: types.Message):
    await message.answer((btc_explorer(message.text.replace('/explorer ', ''))[0] + btc_explorer(message.text.replace('/explorer ', ''))[1] + btc_explorer(message.text.replace('/explorer ', ''))[2]).replace('Balance', 'Баланс').replace('Sent', 'Отправлено').replace('Received', 'Получено'))
    await bot.send_photo(message.from_user.id, btc_explorer(message.text.replace('/explorer ', ''))[3])


@dp.message_handler(commands="altindex", content_types='text')
async def alt_answer(message: types.Message):
    await message.answer('Индекс альтсезона сегодня - ' + alt_index() + '%')

@dp.message_handler(commands="gas")
async def alt_answer(message: types.Message):
    await message.answer('🚀 Быстро - ' + gas()['FastGasPrice'] + ' gwei' + '\n👌Обычно - ' + gas()['ProposeGasPrice'] + ' gwei' + '\n🐢 Медленно - ' + gas()['SafeGasPrice'] + ' gwei')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)