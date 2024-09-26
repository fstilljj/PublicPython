'''
await bot.set_state(call.from_user.id, State.main, call.message.chat.id)
'''
import netmiko
import time
from telebot import asyncio_filters
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot import types
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_filters import AdvancedCustomFilter
from telebot.asyncio_storage import StateMemoryStorage
from telebot.asyncio_handler_backends import State, StatesGroup
from ping3 import ping, verbose_ping
import aioschedule
import ipaddress
API_TOKEN = 'TOKEN'


class PingState(StatesGroup):
    ping = State()
    access = State()
    ac2 = State()
    aut_static = State()
    static = State()
    ans_static = State()
    start_static = State()


PRODUCTS = [
    {'id': '1', 'name': 'Backbone'},
    {'id': '2', 'name': 'Help'}
]



bot = AsyncTeleBot(API_TOKEN, state_storage=StateMemoryStorage())
products_factory = CallbackData('product_id', prefix='products')


def products_keyboard():
    return types.InlineKeyboardMarkup(
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text=product['name'],
                    callback_data=products_factory.new(product_id=product["id"])
                )
            ]
            for product in PRODUCTS
        ]
    )

global authoriz
authoriz = False

class ProductsCallbackFilter(AdvancedCustomFilter):
    key = 'config'

    async def check(self, call: types.CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)

@bot.message_handler(commands=['start'])
async def products_command_handler(message: types.Message):

    await bot.set_state(message.from_user.id, PingState.ping, message.chat.id)
    await bot.send_message(message.chat.id, 'Пройдите авторизацию\nВведите пароль')

@bot.message_handler(state=PingState.ping)
async def proverka(message):
    auth = 'AQ4Qc$xg'
    but = ['IP route']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(*but)
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['logpas'] = message.text
    if data['logpas'] == auth:
        authoriz = True
        await bot.send_message(message.chat.id, 'Приветствую!\nДанный бот умеет :\n\tПроверять ошибки на портах Backbone\n\tЕсть режим поиска данных о точке/точках\nЕсли нужна помощь нажмите на соответствующую кнопку под сообщением', reply_markup = products_keyboard())
        await bot.set_state(message.from_user.id, PingState.access, message.chat.id)
    else:
        await bot.send_message(message.chat.id, 'Неверные данные ')

@bot.message_handler(state=PingState.access, content_types = ['text'])
async def echo_message(message):
    but = ['Отмена']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(*but)
    ans = message.text
    text = ''
    text2 = ''
    ftext = ''
    text_c = 0
    f = open('name2.txt', 'r')
    spis = []
    spis2 = []
    for i in f.read().split('\n\n'):
        spis.append(i)
    for i in spis:
        for k in i.split('\n'):
            if len(ans.lower().split('.')) == 4:
                if ans.lower() == k.lower():
                    text = f'{i}\n'
                    text_c += 1
            else:
                if len(ans.lower().split(' ')) == 1:
                    if ans.lower() in k.lower():
                        if len(text) >= 3000:

                            text2 += f'{i}\n'
                            break
                        else:
                            text += f'{i}\n'
                            text_c += 1
                            break
                elif len(ans.lower().split(' ')) == 2:
                    if ans.lower().split(' ')[0] in k.lower():
                        spis2.append(f'{i}\n')
                        break
    if len(ans.lower().split(' ')) == 2:
        for i in spis2:
            for k in i.split('\n'):
                if ans.lower().split(' ')[1] in k.lower():
                    text += f'{i}\n'
                    text_c += 1
                    break
    f.close()
    print(text_c)
    if text_c == 1:
        if ping(text.split('\n')[3]):
            text += 'Результат Ping удачный'
        else:
            text += 'Результат Ping неудачный'
    if text == '':
        await bot.send_message(message.chat.id, 'Ничего не найдено по вашему запросу', reply_markup=products_keyboard())
    else:
        await bot.send_message(message.chat.id, text, reply_markup=products_keyboard())
    if text2 == '':
        pass
    else:
        await bot.send_message(message.chat.id, text2, reply_markup=products_keyboard())

@bot.callback_query_handler(func=None, config=products_factory.filter(product_id='1'))
async def product_one_callback(call: types.CallbackQuery):
    cisco_router = {
    'device_type': 'eltex',
    'host': '1.1.1.1',
    'username': 'user',
    'password': 'pass',
    'secret': 'pass',
    'port': 22,
    }
    spis = []
    c = 1
    ssh = netmiko.ConnectHandler(**cisco_router)
    text = 'Start checking port...\n'
    for k in range (2):
        for i in range(1, 25):
            a = ssh.send_command(f"sh int count g {c}/0/{i}")
            text += f'gi{c}/0/{i}\n'
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=products_keyboard())
            for h in a.split('\n'):
                if 'Errors' in h:
                    if h.split(': ')[1] != '0':
                        text += f'''{h}\n'''
                        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=products_keyboard())
                        spis.append(f'gi{c}/0/{i}\t{h}')
        c += 1
    if len(spis) != 0:
        text += f'''Error ports:\n'''
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=products_keyboard())
        for i in spis:
            a = i.split('\t')
            text += f'''|{a[0]} {a[1]}|\n'''
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=products_keyboard())
    else:
        text += 'All ports is good'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=products_keyboard())
    text += '''That's all'''
    ssh.disconnect()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=products_keyboard())

@bot.callback_query_handler(func=None, config=products_factory.filter(product_id='2'))
async def product_two_callback(call: types.CallbackQuery):
    text = f'''OPISANIE'''
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=products_keyboard())


bot.add_custom_filter(asyncio_filters.StateFilter(bot))
bot.add_custom_filter(ProductsCallbackFilter())
import asyncio
while True:
        try:
                asyncio.run(bot.polling(none_stop = True, timeout = 10))
        except Exception as e:
                print(e)
                time.sleep(5)
                continue
