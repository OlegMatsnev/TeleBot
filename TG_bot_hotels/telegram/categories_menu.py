from telebot import types
from telebot.types import InlineKeyboardButton

from TG_bot_hotels.hotels_site_API.utils.hotel import Hotel
from bot_setup import bot
from low_high_commands import chose_parameter, high_low_datas
from TG_bot_hotels.hotels_site_API.utils.requests.API_datas_connection.site_api_connector import site
from TG_bot_hotels.hotels_site_API.utils.requests.city_id_request.serchID import url, headers, site


def convert_user_input(user_input: list):
    converted_data = {}

    for item in user_input:
        if 'city' in item:
            city_value = item['city']
            if city_value.isdigit():
                return user_input

    for item in user_input:
        key, value = item.popitem()

        if key == 'rooms':
            converted_rooms = []
            for room in value:
                if not room:
                    print('skip')
                    continue
                adults = int(room.get('adults', 1))
                children_count = int(room.get('children', 0))

                if adults > 0 or children_count > 0:
                    children_list = [{'age': 12} for _ in range(children_count)]

                    room_dict = {
                        'adults': adults,
                        'children': children_list
                    }
                    converted_rooms.append(room_dict)

            converted_data[key] = converted_rooms

        else:
            converted_data[key] = value

        if key == 'city':
            get_city = site.get_city_id()
            city_id = get_city(url=url, headers=headers, city_name=value)
            converted_data[key] = city_id

    convert_to_list = []
    for item in converted_data:
        convert_to_list.append(converted_data[item])

    return convert_to_list


def select_search_category(callback):
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id

    markup = types.InlineKeyboardMarkup()

    low_button = InlineKeyboardButton("low", callback_data="command_low")
    high_button = InlineKeyboardButton("high", callback_data="command_high")
    custom_button = InlineKeyboardButton("custom", callback_data="custom")
    history_button = InlineKeyboardButton("history", callback_data="command_history")
    back_button = InlineKeyboardButton("Назад", callback_data='cont_')

    markup.row(low_button, high_button)
    markup.row(custom_button, history_button)
    markup.row(back_button)


    if callback.data == 'city_':
        bot.edit_message_media(media=types.InputMediaPhoto('https://romani-hotel.ru/wp-content/uploads/2019/11/7380605_0x0.jpg'),
                               chat_id=chat_id, message_id=message_id)

    bot.edit_message_caption(caption='Категории поиска', chat_id=chat_id,
                             reply_markup=markup, message_id=message_id)


def show_hotels_info(callback, hotels):
    ordering_hotels_num = 1

    if not len(callback.data.split('_')) == 3:
        ordering_hotels_num = int(callback.data.split('_')[3])

    hotel: Hotel = hotels[ordering_hotels_num]
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id

    markup = types.InlineKeyboardMarkup()

    print(ordering_hotels_num)
    print(hotel.name)

    if ordering_hotels_num == 1:
        if not len(callback.data.split('_')) == 3:
            callback_left_str = callback.data[:-1] + str(int(callback.data[-1:]))
            callback_right_str = callback.data[:-1] + str(int(callback.data[-1:]) + 1)
        else:
            callback_left_str = callback.data + "_1"
            callback_right_str = callback.data + "_2"

    elif ordering_hotels_num == 5:
        callback_left_str = callback.data[:-1] + str(int(callback.data[-1:]) - 1)
        callback_right_str = callback.data[:-1] + str(int(callback.data[-1:]))

    else:
        callback_left_str = callback.data[:-1] + str(int(callback.data[-1:]) - 1)
        callback_right_str = callback.data[:-1] + str(int(callback.data[-1:]) + 1)

    left_button = InlineKeyboardButton("◀", callback_data=callback_left_str)
    right_button = InlineKeyboardButton("▶", callback_data=callback_right_str)

    if not len(callback.data.split('_')) == 3:
        print(int(callback.data.split('_')[3]))
    # save_hotel = InlineKeyboardButton("Сохранить", callback_data=f"{callback.data}_{ordering_hotels_num}")
    back_button = InlineKeyboardButton("Вернуться в меню", callback_data='city_')
    markup.row(left_button, back_button, right_button)

    bot.edit_message_media(media=types.InputMediaPhoto(f'{hotel.picture_url}'),
                           chat_id=chat_id, message_id=message_id)

    bot.edit_message_caption(caption="Данные об отеле:\n"
                                     "{hotel_data} ".format(hotel_data=hotel),
                             message_id=message_id,
                             chat_id=chat_id,
                             reply_markup=markup)


def make_request(callback):
    command = callback.data.split('_')[1]

    if command == 'low' or command == 'high':
        chose_parameter(callback, command)


    elif command == 'history':
        pass


def get_hotels(callback, user_input):

    sort_type = callback.data.split('_')[1]
    is_high = False
    if sort_type == 'high':
        is_high = True

    category = callback.data.split('_')[2]

    hotels = None

    if category == 'price':
        hotels = high_low_datas(data_list=user_input, high_sort=is_high, is_price=True)
    elif category == 'score':
        hotels = high_low_datas(data_list=user_input, high_sort=is_high, is_scores=True)
    elif category == 'distance':
        hotels = high_low_datas(data_list=user_input, high_sort=is_high, is_distance=True)

    return hotels
