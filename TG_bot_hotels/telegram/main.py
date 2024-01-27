import telebot  # telebot
from pydantic import json
from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup  # States
from telebot import types

from TG_bot_hotels.hotels_site_API.utils.hotel import Hotel
from my_calendar import Calendar
from data_keyboards import get_arrival_year, get_arrival_month, get_arrival_day, user_arrived_data
from data_keyboards import get_departure_year, get_departure_month, get_departure_day, user_departure_data
from rooms import get_rooms_count, get_adults, get_children, room_1, room_2, room_3
from cities import get_country, countries_info
from categories_menu import select_search_category, make_request, get_hotels, show_hotels_info, convert_user_input
from low_high_commands import chose_parameter
from telebot.types import WebAppInfo, ReplyKeyboardMarkup


# States storage
from telebot.storage import StateMemoryStorage

# Now, you can pass storage to bot.
state_storage = StateMemoryStorage()  # you can init here another storage

bot = telebot.TeleBot("6438255358:AAGTFH3DZJS5uubvj7Y26w0UIEZXLATzzsg",
                      state_storage=state_storage)


user_data = [{'checkInDate': None}, {'checkOutDate': None}, {'rooms': None}, {'city': None}]
hotels = []


# https://olegmatsnev.github.io/TeleBot/index.html


@bot.message_handler(commands=['start'])
def start_ex(message):
    print('start_ex')

    markup = types.InlineKeyboardMarkup()

    # Добавляем кнопку "Открыть веб страницу" с URL-адресом
    web_app_button = types.InlineKeyboardButton("Открыть веб страницу",
                                                url='https://olegmatsnev.github.io/TeleBot/index.html')

    markup.add(web_app_button)

    # Отправляем сообщение с инлайн-клавиатурой
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)


@bot.message_handler(content_types="web_app_data") #получаем отправленные данные
def answer(webAppMes):
   print(webAppMes) #вся информация о сообщении
   print(webAppMes.web_app_data.data) #конкретно то что мы передали в бота
   bot.send_message(webAppMes.chat.id, f"получили инофрмацию из веб-приложения: {webAppMes.web_app_data.data}")
   #отправляем сообщение в ответ на отправку данных из веб-приложения


@bot.callback_query_handler(func=lambda call: call.data == 'search_hotels')
def get_year(callback):
    get_arrival_year(callback)


@bot.callback_query_handler(func=lambda call: call.data.startswith('year_'))
def get_month(callback):
    get_arrival_month(callback)


@bot.callback_query_handler(func=lambda call: call.data.startswith('month_'))
def get_day(callback):
    get_arrival_day(callback)


"""Departure data"""


@bot.callback_query_handler(func=lambda call: call.data.startswith('day_'))
def get_dep_year(callback):
    get_departure_year(callback)
    print(user_arrived_data)


@bot.callback_query_handler(func=lambda call: call.data.startswith('departure_year_'))
def get_dep_month(callback):
    get_departure_month(callback)


@bot.callback_query_handler(func=lambda call: call.data.startswith('departure_month_'))
def get_dep_day(callback):
    get_departure_day(callback)


"""Rooms"""


@bot.callback_query_handler(func=lambda call: call.data.startswith('departure_day_'))
def rooms_count(callback):
    if user_departure_data.get('day', None) is None:
        selected_day = int(callback.data.split('_')[2])
        user_departure_data['day'] = selected_day
    else:
        if callback.data.split('_')[2] != '':
            selected_day = int(callback.data.split('_')[2])
            user_departure_data['day'] = selected_day

    print(f'Дата отъезда {user_departure_data}')
    print(f'Дата приезда {user_arrived_data}')

    get_rooms_count(callback=callback)


@bot.callback_query_handler(func=lambda call: call.data.startswith('rooms_count_'))
def room_adults_count(callback):
    get_adults(callback=callback)


@bot.callback_query_handler(func=lambda call: call.data.startswith('adults_count_'))
def room_children_count(callback):
    get_children(callback=callback)


"""City"""


@bot.callback_query_handler(func=lambda call: call.data.startswith('cont_'))
def chose_country(callback):

    if callback.data.split('_')[1].isdigit():
        last_children_room_filling = callback.data.split('_')[1]
        room_1['children'] = last_children_room_filling
        print('Finish', room_1, room_2, room_3)
        callback.data = "cont_Europe_country_Italy"
        print(callback.data)
    elif callback.data == 'cont_':
        callback.data = "cont_Europe_country_Italy"
        print('here')
    get_country(callback=callback)


@bot.callback_query_handler(func=lambda call: call.data == 'countries_info')
def counties_info_menu(callback):
    countries_info(callback)


@bot.callback_query_handler(func=lambda call: call.data.startswith('city_'))
def search_category(callback):

    global user_data
    if callback.data != 'city_':
        city = callback.data.split('_')[1]
        user_data[0]['checkInDate'] = user_arrived_data
        user_data[1]['checkOutDate'] = user_departure_data
        user_data[2]['rooms'] = [room_1, room_2, room_3]
        user_data[3]['city'] = city
        user_data = convert_user_input(user_data)

    select_search_category(callback=callback)


"""Commands"""



@bot.callback_query_handler(func=lambda call: call.data.startswith('command_'))
def search_category(callback):
    make_request(callback)


@bot.callback_query_handler(func=lambda call: call.data.startswith('category_'))
def show_hotels(callback):

    global hotels
    if len(callback.data.split('_')) == 3:
        hotels = get_hotels(callback=callback, user_input=user_data)

    show_hotels_info(callback, hotels)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    print('fsa')
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if call.data == 'instruction':
        markup = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton("Назад", callback_data='back')
        markup.row(back_button)
        bot.edit_message_media(media=types.InputMediaPhoto('https://bnovo.ru/wp-content/uploads/2021/11/registration'
                                                           '-of-guests-at-the-hotel-4-800.jpg'),
                               chat_id=chat_id, message_id=message_id)
        bot.edit_message_caption(caption='Это инструкция, здесь должен быть ваш текст инструкции.', chat_id=chat_id,
                                 reply_markup=markup, message_id=message_id)
    elif call.data == 'website':
        markup = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton("Назад", callback_data='back')
        markup.row(back_button)
        bot.edit_message_caption(caption='Это ваш веб-сайт, здесь должен быть текст о сайте.', chat_id=chat_id,
                                 reply_markup=markup, message_id=message_id)

    elif call.data == 'back':
        markup = types.InlineKeyboardMarkup()
        item1 = types.InlineKeyboardButton("Инструкция", callback_data='instruction')
        item2 = types.InlineKeyboardButton("Сайт", callback_data='website')
        markup.row(item1, item2)
        item3 = types.InlineKeyboardButton("Поиск отелей", callback_data='search_hotels')
        markup.row(item3)
        bot.edit_message_media(media=types.InputMediaPhoto('https://romani-hotel.ru/wp-content/uploads/2019/11/7380605_0x0.jpg'),
                               chat_id=chat_id, message_id=message_id)
        bot.edit_message_caption(caption='Главное меню.', chat_id=chat_id,
                                 reply_markup=markup, message_id=message_id)


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())

bot.infinity_polling(skip_pending=True)


# Дата отъезда {'year': 2024, 'month': 2, 'day': 14}
# Дата приезда {'year': 2024, 'month': 2, 'day': 7}
# {'adults': '2', 'children': '1'} {'adults': '2', 'children': '1'} {}
# Belek

# [
#   {'checkInDate': {'year': 2024, 'month': 5, 'day': 14}},
#   {'checkOutDate': {'year': 2024, 'month': 9, 'day': 20}},
#   {'rooms': [{'adults': '2', 'children': '2'}, {'adults': '2', 'children': '1'}, {}]},
#   {'city': 'Ottawa'}
# ]
