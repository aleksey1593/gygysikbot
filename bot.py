import asyncio
import logging
import aioschedule
import os

from sql import Dbase
from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import KeyboardButton
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import ReplyKeyboardMarkup
from parsing import uznat, banki_kursi


API_TOKEN = os.environ['TOKEN']
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# клавиатура
button_USD_prodaza = KeyboardButton('USD продаю')
button_USD_pokupka = KeyboardButton('USD покупаю')
button_EUR_prodaza = KeyboardButton('EUR продаю')
button_EUR_pokupka = KeyboardButton('EUR покупаю')
board = ReplyKeyboardMarkup(resize_keyboard=True).row(button_USD_prodaza, button_USD_pokupka).row(button_EUR_prodaza, button_EUR_pokupka)


bot_db = Dbase()
bot_db.create_table()

# для рассылки
def course_act():
    course = uznat()
    Dollar = course['USD']
    EURO = course['EUR']
    text = f'курс USD: {Dollar}, курс EURO:{EURO}'
    return text


@dp.message_handler(commands='kurs')
async def welcome(message: types.Message):
    await message.answer(course_act())


@dp.message_handler(commands='podpiska')
async def welcome(message: types.Message):
    idtel = int(message.from_user.id)
    user_info = (message.from_user.first_name, message.from_user.last_name, idtel, 1)
    if not bot_db.user_exists((message.from_user.first_name, message.from_user.last_name, idtel)):
        bot_db.add_user(user_info)
    else:
        bot_db.obnovit_podpisky((idtel,))
    text = f'Спасибо! Рассылка курсов будет каждый день в 13:00'
    await message.answer(text)

@dp.message_handler(commands='otpiska')
async def welcome(message: types.Message):
    idtel = int(message.from_user.id)
    if not bot_db.user_exists((message.from_user.first_name, message.from_user.last_name, idtel)):
        text = f'Вы и не подписывались:)'
    else:
        bot_db.otpiska((idtel,))
        text = f'Вы отписаны.'
    await message.answer(text)










@dp.message_handler(commands='start')
async def welcome(message: types.Message):
    text = f'Привет, {message.from_user.full_name}! Напиши /help чтобы узнать, что я могу)'
    await message.answer(text)


@dp.message_handler(commands='help')
async def help(message: types.Message):
    text = f"""Вызовите команду "/kurs" чтобы узнать курсы НБ РБ, 
вызовите команду "/podpiska" чтобы подписаться на рассылку курсов НБ РБ,
вызовите команду "/otpiska" чтобы отказаться от рассылки,
вызовите команду "/komkurs"чтобы узнать лучшие коммерческие курсы на данный момент."""
    await message.answer(text)


@dp.message_handler(commands='komkurs')
async def menu(message: types.Message):
    await message.answer('Выберите операцию', reply_markup=board)

@dp.message_handler(Text(equals='USD продаю'))
async def privet(message: types.Message):
    otvet = ''
    banki = banki_kursi('продажа', 'USD')
    for i in range(len(banki)):
        otvet += f'{i+1}) {banki[i]} \n'
    await message.answer(otvet, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(Text(equals='USD покупаю'))
async def privet(message: types.Message):
    otvet = ''
    banki = banki_kursi('покупка', 'USD')
    for i in range(len(banki)):
        otvet += f'{i+1}) {banki[i]} \n'
    await message.answer(otvet, reply_markup=ReplyKeyboardRemove())

@dp.message_handler(Text(equals='EUR продаю'))
async def privet(message: types.Message):
    otvet = ''
    banki = banki_kursi('продажа', 'EUR')
    for i in range(len(banki)):
        otvet += f'{i+1}) {banki[i]} \n'
    await message.answer(otvet, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(Text(equals='EUR покупаю'))
async def privet(message: types.Message):
    otvet = ''
    banki = banki_kursi('покупка', 'EUR')
    for i in range(len(banki)):
        otvet += f'{i+1}) {banki[i]} \n'
    await message.answer(otvet, reply_markup=ReplyKeyboardRemove())


@dp.message_handler()
async def vozvrat_k_help(message: types.Message):
    await message.answer("Не понял тебя, воспользуйся командой /help чтобы узнать что я умею")


async def rassylka():
    for id in bot_db.all_users():
        await bot.send_message(id[0], course_act())


async def scheduler():
    aioschedule.every().day.at("10:00").do(rassylka)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(x):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
