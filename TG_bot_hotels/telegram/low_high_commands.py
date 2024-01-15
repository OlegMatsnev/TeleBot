
from telebot import types
from telebot.types import InlineKeyboardButton


from TG_bot_hotels.hotels_site_API.utils.hotel import Hotel
from bot_setup import bot
from TG_bot_hotels.hotels_site_API.utils.requests.API_datas_connection.site_api_connector import url, headers, site_api
from TG_bot_hotels.hotels_site_API.utils.hotel import Hotel


get_hotels = site_api.get_hotels()


def del_unpopular_hotels(hotels: list[Hotel]):
    """
        Функция фильтрует отели, оставляя только те, у которых больше 10 отзывов.

        Args:
            hotels (list[Hotel]): Список объектов типа Hotel.

        Returns:
            :return new_list (filtered list)
            :rtype list[Hotel]: Отфильтрованный список отелей с более чем 10 отзывами.
        """

    new_list: list[Hotel] = []

    for hotel in hotels:
        if hotel.reviews_count >= 10:
            new_list.append(hotel)

    return new_list


def high_low_datas(data_list: list, high_sort=False, count_hotels=5,
                   is_price=False, is_scores=False, is_distance=False) -> (list[Hotel], None):

    """
    Функция сортирует отели по различным критериям.

    Args:
        data_list (list): Список данных о поиске (дата приезда, дата отъезда, комнаты и город).
        high_sort (bool): Сортировать по убыванию (если True) или по возрастанию (если False).
        count_hotels (int): Количество отелей для выбора (по умолчанию = 5).
        is_price (bool): Сортировать по цене.
        is_scores (bool): Сортировать по рейтингу отелей.
        is_distance (bool): Сортировать по расстоянию до центра.

    Returns:
        :return sorted list
        :rtype list[Hotel]: list[Hotel] or None: ->
        -> Отсортированный список отелей или None, если не указан ни один критерий сортировки.
    """

    print('hereeeee')
    print(data_list)

    if is_price:
        all_city_hotels = get_hotels(url=url, headers=headers, data_list=data_list, sort="PRICE_LOW_TO_HIGH")
        if high_sort:
            all_city_hotels.reverse()
            return all_city_hotels
        else:
            return all_city_hotels

    if is_scores:
        all_city_hotels = get_hotels(url=url, headers=headers, data_list=data_list, sort="REVIEW")
        only_popular_reviews_list = del_unpopular_hotels(all_city_hotels)
        scores_sorted_hotels_list = sorted(only_popular_reviews_list, key=lambda hotel: hotel.reviews_score,
                                           reverse=high_sort)
        return scores_sorted_hotels_list

    if is_distance:
        all_city_hotels = get_hotels(url=url, headers=headers, data_list=data_list, sort="DISTANCE")
        if high_sort:
            return all_city_hotels
        else:
            all_city_hotels.reverse()
            return all_city_hotels


def chose_parameter(callback, category_str):
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id

    markup = types.InlineKeyboardMarkup()

    price_button = InlineKeyboardButton("Цена", callback_data=f"category_{category_str}_price")
    score_button = InlineKeyboardButton("Оценка", callback_data=f"category_{category_str}_score")
    distance_button = InlineKeyboardButton("Центр", callback_data=f"category_{category_str}_distance")

    back_button = InlineKeyboardButton("Назад", callback_data="city_")
    markup.row(price_button, score_button, distance_button)
    markup.row(back_button)

    bot.edit_message_caption(caption="Выберите параметр подбора отелей: ",
                             message_id=message_id,
                             chat_id=chat_id,
                             reply_markup=markup)
