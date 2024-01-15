from my_calendar import Calendar
from telebot import types
from bot_setup import bot

user_arrived_data = {}
user_departure_data = {}


def get_arrival_year(callback):
    print('year')
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id

    year_markup = Calendar()
    markup = year_markup.create_years_calendar()
    back_button = types.InlineKeyboardButton("Назад", callback_data='back')
    markup.row(back_button)
    bot.edit_message_caption(caption='Выберите год прибытия в отель:', chat_id=chat_id,
                             reply_markup=markup, message_id=message_id)


def get_arrival_month(callback):
    print('month')
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id

    if user_arrived_data.get('year', None) is None:
        selected_year = int(callback.data.split('_')[1])
        user_arrived_data['year'] = selected_year
    else:
        if callback.data.split('_')[1] != '':
            selected_year = int(callback.data.split('_')[1])
            user_arrived_data['year'] = selected_year

    month_markup = Calendar()
    markup = month_markup.create_months_calendar(user_arrived_data['year'])
    back_button = types.InlineKeyboardButton("Назад", callback_data='search_hotels')
    markup.row(back_button)
    bot.edit_message_caption(caption='Выберите месяц прибытия в отель:', chat_id=chat_id,
                             reply_markup=markup, message_id=message_id)


def get_arrival_day(callback):
    print('day')
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id

    print(callback.data)

    if user_arrived_data.get('month', None) is None:
        selected_month = int(callback.data.split('_')[1])
        user_arrived_data['month'] = selected_month
    else:
        if callback.data.split('_')[1] != '':
            selected_month = int(callback.data.split('_')[1])
            user_arrived_data['month'] = selected_month

    day_markup = Calendar()
    markup = day_markup.create_days_calendar(user_arrived_data['year'], user_arrived_data['month'])
    back_button = types.InlineKeyboardButton("Назад", callback_data='year_')
    markup.row(back_button)
    bot.edit_message_caption(caption='Выберите день прибытия в отель:', chat_id=chat_id,
                             reply_markup=markup, message_id=message_id)


def get_departure_year(callback):
    print('departure_year')
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id

    if user_arrived_data.get('day', None) is None:
        selected_day = int(callback.data.split('_')[1])
        user_arrived_data['day'] = selected_day
    else:
        if callback.data.split('_')[1] != '':
            selected_day = int(callback.data.split('_')[1])
            user_arrived_data['day'] = selected_day

    year_markup = Calendar()
    markup = year_markup.create_departure_years_calendar(
        arrived_year=user_arrived_data['year'],
        arrived_month=user_arrived_data['month'],
        arrived_day=user_arrived_data['day'])

    back_button = types.InlineKeyboardButton("Назад", callback_data='month_')
    markup.row(back_button)
    bot.edit_message_caption(caption='Выберите год отбытия из отеля:', chat_id=chat_id,
                             reply_markup=markup, message_id=message_id)


def get_departure_month(callback):
    print('departure_month')
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id

    if user_departure_data.get('year', None) is None:
        selected_year = int(callback.data.split('_')[2])
        user_departure_data['year'] = selected_year
    else:
        if callback.data.split('_')[2] != '':
            selected_year = int(callback.data.split('_')[2])
            user_departure_data['year'] = selected_year

    month_markup = Calendar()
    markup = month_markup.create_departure_month_calendar(
        departure_year=user_departure_data['year'],
        arrived_year=user_arrived_data['year'],
        arrived_month=user_arrived_data['month'],
        arrived_day=user_arrived_data['day']
    )
    back_button = types.InlineKeyboardButton("Назад", callback_data='day_')
    markup.row(back_button)
    bot.edit_message_caption(caption='Выберите месяц отбытия из отеля:', chat_id=chat_id,
                             reply_markup=markup, message_id=message_id)


def get_departure_day(callback):
    print('departure_day')
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id

    if user_departure_data.get('month', None) is None:
        selected_month = int(callback.data.split('_')[2])
        user_departure_data['month'] = selected_month
    else:
        if callback.data.split('_')[2] != '':
            selected_month = int(callback.data.split('_')[2])
            user_departure_data['month'] = selected_month

    day_markup = Calendar()
    markup = day_markup.create_departure_days_calendar(
        departure_year=user_departure_data['year'],
        departure_month=user_departure_data['month'],
        arrived_year=user_arrived_data['year'],
        arrived_month=user_arrived_data['month'],
        arrived_day=user_arrived_data['day']
    )
    back_button = types.InlineKeyboardButton("Назад", callback_data='departure_year_')
    markup.row(back_button)
    bot.edit_message_caption(caption='Выберите день отбытия из отеля:', chat_id=chat_id,
                             reply_markup=markup, message_id=message_id)