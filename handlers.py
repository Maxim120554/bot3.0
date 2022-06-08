from create_bot import bot, dp
from aiogram import types, Dispatcher
from bs4 import BeautifulSoup
import requests, database, keyboards
from fake_useragent import UserAgent
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class FSM(StatesGroup):
    name = State()





# @dp.message_handler(commands=['start', 'help'])
async def answer_start(message: types.Message):
    # markup = keyboards.create_keyboard('Узнать_о_монетах', 'Добавить_в_избранное', 'Очистить_избранное')
    await bot.send_message(message.from_user.id, f'Привет, {message.from_user.first_name}',
                           reply_markup=keyboards.create_kb('/Узнать_о_монетах'))
    await database.sql_add_command(message)


# @dp.message_handler(commands=['Очистить_избранное'])
async def clear_favorites(message: types.Message):
    pass


# @dp.message_handler(commands=['Узнать_о_монетах'])
async def learn_about(message: types.Message):
    await FSM.name.set()
    await message.reply('Введите название монеты')


@dp.message_handler(commands=['Назад'], state=FSM.name)
async def back(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id, ':)', reply_markup=keyboards.create_kb('/Узнать_о_монетах'))


# @dp.message_handler(state=FSM.name)
async def get_info(message: types.Message):
    ua = UserAgent()
    headers = {
        'accept': '* / *',
        'UserAgent': ua.random
    }
    try:
        text = message.text.replace(' ', '-')
        req = requests.get(f'https://coinmarketcap.com/currencies/{text.lower()}/markets/', headers=headers)
        soup = BeautifulSoup(req.text, 'lxml')
        symbol = soup.find('small', class_='nameSymbol').text
        price = soup.find('div', class_='priceValue').text
        market_cap = soup.find('div', class_='statsValue').text
        max_supply = soup.find_all('div', class_='maxSupplyValue')[0].text
        total_supply = soup.find_all('div', class_='maxSupplyValue')[1].text
        kb = InlineKeyboardMarkup()
        btn = InlineKeyboardButton(text='Добавить в избранное', callback_data='add_to_favorites')
        kb.insert(btn)
        await bot.send_message(message.chat.id,
                               f"""{symbol}\n
Цена: {price}\n
Капитализация: {market_cap}\n\nПодробную информацию смотри по ссылке\n\n
https://coinmarketcap.com/currencies/{text.lower()}/markets/""", reply_markup=kb)
    except requests.exceptions.MissingSchema:
        await bot.send_message(message.chat.id, 'Введите корректное название')
    except AttributeError:
        await bot.send_message(message.chat.id, 'Введите корректное название')


@dp.callback_query_handler(text='add_to_favorites')
async def add_to_favorites(message: types.Message, call: types.CallbackQuery):
    await call.answer('Монета якобы добавлена')


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(answer_start, commands=['start', 'help'])
    dp.register_message_handler(clear_favorites, commands=['Очистить_избранное'])
    dp.register_message_handler(learn_about, commands=['Узнать_о_монетах'], state=None)
    dp.register_message_handler(get_info, state=FSM.name)
    dp.register_message_handler(back, state=FSM.name)


