from telebot import types
from telebot.types import InlineKeyboardButton
from bot_setup import bot

room_1 = {}
room_2 = {}
room_3 = {}


def get_rooms_count(callback):
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id

    markup = types.InlineKeyboardMarkup()

    rooms_count_1 = InlineKeyboardButton(str(1), callback_data='rooms_count_1_c')
    rooms_count_2 = InlineKeyboardButton(str(2), callback_data='rooms_count_2_c')
    rooms_count_3 = InlineKeyboardButton(str(3), callback_data='rooms_count_3_c')

    markup.row(rooms_count_1, rooms_count_2, rooms_count_3)

    back_button = types.InlineKeyboardButton("Назад", callback_data='departure_month_')
    markup.row(back_button)

    bot.edit_message_caption(caption='Количество требуемых комнат:', chat_id=chat_id,
                             reply_markup=markup, message_id=message_id)


def get_adults(callback):

    chat_id = callback.message.chat.id
    message_id = callback.message.message_id

    markup = types.InlineKeyboardMarkup()

    if callback.data.split('_')[3] == '':
        rooms_count = callback.data.split('_')[2]
    else:
        if callback.data.split('_')[3] == 'c':
            rooms_count = callback.data.split('_')[2]
        else:
            rooms_count = int(callback.data.split('_')[2])

            if rooms_count == 0:
                room_1["children"] = callback.data.split('_')[3]
            elif rooms_count == 1:
                room_2["children"] = callback.data.split('_')[3]
            elif rooms_count == 2:
                room_3["children"] = callback.data.split('_')[3]

    print(f'Вывод данных о комнатах. '
          f'\nКомната 3 {room_3}'
          f'\nКомната 2 {room_2}'
          f'\nКомната 1 {room_1}')

    adults_count_1 = InlineKeyboardButton(str(1), callback_data=f'adults_count_1_{rooms_count}')
    adults_count_2 = InlineKeyboardButton(str(2), callback_data=f'adults_count_2_{rooms_count}')
    adults_count_3 = InlineKeyboardButton(str(3), callback_data=f'adults_count_3_{rooms_count}')
    adults_count_4 = InlineKeyboardButton(str(4), callback_data=f'adults_count_4_{rooms_count}')
    markup.row(adults_count_1, adults_count_2, adults_count_3, adults_count_4)

    if callback.data.split('_')[3] == 'c':
        back_button = types.InlineKeyboardButton("Назад", callback_data='departure_day_')
    else:
        prev_room = int(callback.data.split('_')[2]) + 1
        back_button = types.InlineKeyboardButton("Назад", callback_data=f'adults_count_{prev_room}')
    markup.row(back_button)

    bot.edit_message_caption(caption=f'Количество взрослых в комнате номер {rooms_count}:', chat_id=chat_id,
                             reply_markup=markup, message_id=message_id)


def get_children(callback):
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id

    markup = types.InlineKeyboardMarkup()

    if len(callback.data.split('_')) == 3:
        rooms_count = int(callback.data.split('_')[2])
    else:
        rooms_count = int(callback.data.split('_')[3])

        # записываем взрослых в нужную комнату
        if rooms_count == 1:
            room_1["adults"] = callback.data.split('_')[2]
        elif rooms_count == 2:
            room_2["adults"] = callback.data.split('_')[2]
        elif rooms_count == 3:
            room_3["adults"] = callback.data.split('_')[2]

    rooms_count -= 1

    # если комната последняя, то после выбора детей в последнюю комнату - перемещаемся к выбору континента
    if rooms_count == 0:

        children_count_1 = InlineKeyboardButton(str(0), callback_data=f'cont_0')
        children_count_2 = InlineKeyboardButton(str(1), callback_data=f'cont_1')
        children_count_3 = InlineKeyboardButton(str(2), callback_data=f'cont_2')
        children_count_4 = InlineKeyboardButton(str(3), callback_data=f'cont_3')
        markup.row(children_count_1, children_count_2, children_count_3, children_count_4)

        back_button = types.InlineKeyboardButton("Назад", callback_data=f'rooms_count_{rooms_count + 1}_')
        markup.row(back_button)

        bot.edit_message_caption(caption=f'Количество детей в комнате номер {rooms_count + 1}:', chat_id=chat_id,
                                 reply_markup=markup, message_id=message_id)
    else:

        children_count_1 = InlineKeyboardButton(str(0), callback_data=f'rooms_count_{rooms_count}_0')
        children_count_2 = InlineKeyboardButton(str(1), callback_data=f'rooms_count_{rooms_count}_1')
        children_count_3 = InlineKeyboardButton(str(2), callback_data=f'rooms_count_{rooms_count}_2')
        children_count_4 = InlineKeyboardButton(str(3), callback_data=f'rooms_count_{rooms_count}_3')
        markup.row(children_count_1, children_count_2, children_count_3, children_count_4)

        back_button = types.InlineKeyboardButton("Назад", callback_data=f'rooms_count_{rooms_count + 1}_')
        markup.row(back_button)

        bot.edit_message_caption(caption=f'Количество детей в комнате номер {rooms_count + 1}:', chat_id=chat_id,
                                 reply_markup=markup, message_id=message_id)

