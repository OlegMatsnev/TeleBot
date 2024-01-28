from TG_bot_hotels.hotels_site_API.utils.hotel import Hotel
from TG_bot_hotels.hotels_site_API.utils.requests.API_datas_connection.site_api_connector import site_api, headers, url

get_hotels = site_api.get_hotels()


def correct_filter_data(filter_data: dict):
    stars_list = []
    min_star = filter_data["star"]
    if min_star == 2:
        stars_list = ["20", "30", "40", "50"]
    elif min_star == 3:
        stars_list = ["30", "40", "50"]
    elif min_star == 4:
        stars_list = ["40", "50"]
    elif min_star == 5:
        stars_list = ["50"]

    filter_data["star"] = stars_list


def custom(data_list: list, filter_data: dict, count_hotels=7):
    """
        Основная функция для выбора отелей на основе пользовательских критериев.

        Args:
            data_list (list): Список данных о поиске (например, дата приезда, дата отъезда, комнаты и город).
            count_hotels (int): Количество отелей для выбора.
            price_filter (bool): Фильтровать ли по цене.
            stars_filter (bool): Фильтровать ли по количеству звёзд.
            pool_filter (bool): Фильтровать ли по наличию бассейна.

        Ex:
            {
    "currency": "USD",
    "eapid": 1,
    "locale": "en_US",
    "siteId": 300000001,
    "destination": {
        "regionId": "6054439"
    },
    "checkInDate": {
        "day": 10,
        "month": 10,
        "year": 2022
    },
    "checkOutDate": {
        "day": 15,
        "month": 10,
        "year": 2022
    },
    "rooms": [
        {
            "adults": 2,
            "children": [
                {
                    "age": 5
                },
                {
                    "age": 7
                }
            ]
        }
    ],
    "resultsStartingIndex": 0,
    "resultsSize": 200,
    "sort": "PRICE_LOW_TO_HIGH",
    "filters": {
        "price": {
            "max": 150,
            "min": 100
        },
        "guestRating": "35",
        "star": ["40","50"]
    }
}

        Returns:
            list[Hotel]: Список выбранных отелей.
        """



    all_city_hotels = get_hotels(url=url, headers=headers, data_list=data_list,
                                     filters=filter_data)

    return all_city_hotels[:count_hotels]

        # all_city_hotels = get_hotels(url=url, headers=headers, data_list=data_list,
        #                              filters={"star": [stars_hotel_count]})
        #
        # all_city_hotels = get_hotels(url=url, headers=headers, data_list=data_list,
        #                              filters={"amenities": ["POOL"]})
