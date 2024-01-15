from telebot import types
import datetime
from telebot.types import InlineKeyboardButton
import calendar


class Calendar:
    def __init__(self):
        now = datetime.datetime.now()
        self.current_year = now.year
        self.current_month = now.month
        self.current_day = now.day

    def create_years_calendar(self):
        markup = types.InlineKeyboardMarkup()
        current_year_btn = types.InlineKeyboardButton(str(self.current_year), callback_data=f'year_{self.current_year}')
        next_year_btn = types.InlineKeyboardButton(str(self.current_year + 1),
                                                   callback_data=f'year_{self.current_year + 1}')
        markup.add(current_year_btn, next_year_btn)
        return markup

    def create_months_calendar(self, year: int):

        months = ['январь', 'февраль', 'март',
                  'апрель', 'май', 'июнь',
                  'июль', 'август', 'сентябрь',
                  'октябрь', 'ноябрь', 'декабрь']

        markup = types.InlineKeyboardMarkup()

        if year == self.current_year:
            row_buttons_lst: list[InlineKeyboardButton] = []
            start_month = self.current_month

            last_day = datetime.date(self.current_year, self.current_month,
                                     calendar.monthrange(self.current_year, self.current_month)[1])
            if self.current_day == last_day.day:
                start_month = self.current_month + 1

            for i in range(start_month, 13):
                cur_month = types.InlineKeyboardButton(months[i - 1], callback_data=f'month_{i}')
                row_buttons_lst.append(cur_month)
                if len(row_buttons_lst) == 3:
                    markup.row(*row_buttons_lst)
                    row_buttons_lst = []
            if len(row_buttons_lst) != 0:
                markup.row(*row_buttons_lst)

        elif year == self.current_year + 1:
            for i in range(1, 13, 3):
                cur_month_1 = types.InlineKeyboardButton(months[i - 1], callback_data=f'month_{i}')
                cur_month_2 = types.InlineKeyboardButton(months[i], callback_data=f'month_{i + 1}')
                cur_month_3 = types.InlineKeyboardButton(months[i + 1], callback_data=f'month_{i + 2}')
                markup.row(cur_month_1, cur_month_2, cur_month_3)

        else:
            return None

        return markup

    def create_days_calendar(self, year, month):

        first_day = datetime.date(year, month, 1)
        last_day = datetime.date(year, month, calendar.monthrange(year, month)[1])
        days_in_month = (last_day - first_day).days + 1

        markup = types.InlineKeyboardMarkup()
        weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

        # Добавляем верхний ряд с днями недели
        markup.row(*[types.InlineKeyboardButton(day, callback_data="empty") for day in weekdays])

        if year == self.current_year and month == self.current_month:
            start_day = self.current_day + 1

            date = datetime.date(year, month, start_day)  # дата
            day_of_week_number = date.weekday()  # номер дня недели

            days_in_first_row = 7 - day_of_week_number
            rows_count = ((days_in_month - days_in_first_row - (start_day - 1)) // 7) + 1

            row_buttons_lst = []

            for day_i in range(7):
                if start_day - day_of_week_number + day_i > days_in_month:
                    break

                if day_i < day_of_week_number:
                    row_buttons_lst.append(types.InlineKeyboardButton("\u200B", callback_data="empty"))
                else:
                    row_buttons_lst.append(types.InlineKeyboardButton(str(start_day - day_of_week_number + day_i),
                                                                      callback_data=f'day_{str(start_day - day_of_week_number + day_i)}'))

            markup.row(*row_buttons_lst)
            row_buttons_lst = []

            for row_i in range(rows_count):
                current_day = start_day + days_in_first_row + (7 * row_i)
                for day_i in range(7):
                    if day_i + current_day <= days_in_month:
                        row_buttons_lst.append(types.InlineKeyboardButton(str(day_i + current_day),
                                                                          callback_data=f'day_{str(day_i + current_day)}'))
                    else:
                        row_buttons_lst.append(types.InlineKeyboardButton("\u200B", callback_data="empty"))
                markup.row(*row_buttons_lst)
                row_buttons_lst = []

            return markup

        else:
            current_weekday = calendar.weekday(year, month, 1)  # номер дня недели первого числа
            current_day = 1

            # Так как дата отъезда должна быть на 1 день как минимум позже даты приезда,
            # то добавлена проверка на последний день последнего года (из предложенных) последнего месяца,
            # чтобы пользователь не смог выбрать дату из следующего недоступного года или выбрать тот же день отъезда
            if year == self.current_year + 1 and month == 12:
                days_in_month -= 1

            # Добавляем дни месяца в ячейки
            while current_day <= days_in_month:
                row_buttons_lst = []
                for _ in range(current_weekday):
                    row_buttons_lst.append(types.InlineKeyboardButton("\u200B", callback_data="empty"))

                while current_weekday < 7 and current_day <= days_in_month:
                    row_buttons_lst.append(
                        types.InlineKeyboardButton(str(current_day), callback_data=f'day_{str(current_day)}'))
                    current_day += 1
                    current_weekday += 1
                while current_weekday < 7:
                    row_buttons_lst.append(types.InlineKeyboardButton("\u200B", callback_data="empty"))
                    current_weekday += 1

                markup.row(*row_buttons_lst)
                current_weekday = 0

            return markup

    def create_departure_years_calendar(self, arrived_year, arrived_month, arrived_day):
        markup = types.InlineKeyboardMarkup()

        if not (arrived_year == self.current_year and arrived_month == 12 and arrived_day == 31) \
                and arrived_year == self.current_year:

            current_year_btn = types.InlineKeyboardButton(str(self.current_year),
                                                          callback_data=f'departure_year_{self.current_year}')
            next_year_btn = types.InlineKeyboardButton(str(self.current_year + 1),
                                                       callback_data=f'departure_year_{self.current_year + 1}')
            markup.add(current_year_btn, next_year_btn)

        else:
            next_year_btn = types.InlineKeyboardButton(str(self.current_year + 1),
                                                       callback_data=f'departure_year_{self.current_year + 1}')
            markup.add(next_year_btn)

        return markup

    def create_departure_month_calendar(self, departure_year, arrived_year, arrived_month, arrived_day):

        months = ['январь', 'февраль', 'март',
                  'апрель', 'май', 'июнь',
                  'июль', 'август', 'сентябрь',
                  'октябрь', 'ноябрь', 'декабрь']

        markup = types.InlineKeyboardMarkup()

        if departure_year == arrived_year + 1:
            for i in range(1, 13, 3):
                cur_month_1 = types.InlineKeyboardButton(months[i - 1], callback_data=f'departure_month_{i}')
                cur_month_2 = types.InlineKeyboardButton(months[i], callback_data=f'departure_month_{i + 1}')
                cur_month_3 = types.InlineKeyboardButton(months[i + 1], callback_data=f'departure_month_{i + 2}')
                markup.row(cur_month_1, cur_month_2, cur_month_3)

        else:

            # Получаем последний день месяца
            last_day = calendar.monthrange(arrived_year, arrived_month)[1]

            if last_day == arrived_day:
                arrived_month += 1

            row_buttons_lst: list[InlineKeyboardButton] = []
            for i in range(arrived_month, 13):
                cur_month = types.InlineKeyboardButton(months[i - 1], callback_data=f'departure_month_{i}')
                row_buttons_lst.append(cur_month)
                if len(row_buttons_lst) == 3:
                    markup.row(*row_buttons_lst)
                    row_buttons_lst = []
            if len(row_buttons_lst) != 0:
                markup.row(*row_buttons_lst)

        return markup

    def create_departure_days_calendar(self, departure_year, departure_month, arrived_year, arrived_month, arrived_day):

        first_day = datetime.date(departure_year, departure_month, 1)
        last_day = datetime.date(departure_year, departure_month,
                                 calendar.monthrange(departure_year, departure_month)[1])
        days_in_month = (last_day - first_day).days + 1

        # если последний день месяца - то возвращаем null (уже номера забронированы)
        if departure_year == self.current_year and departure_month == self.current_month and \
                self.current_day == last_day.day:
            return None

        markup = types.InlineKeyboardMarkup()
        weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

        # Добавляем верхний ряд с днями недели
        markup.row(*[types.InlineKeyboardButton(day, callback_data="empty") for day in weekdays])

        if departure_year == arrived_year and departure_month == arrived_month:
            start_day = arrived_day + 1

            date = datetime.date(departure_year, departure_month, start_day)  # дата
            day_of_week_number = date.weekday()  # номер дня недели

            days_in_first_row = 7 - day_of_week_number
            rows_count = ((days_in_month - days_in_first_row - (start_day - 1)) // 7) + 1

            row_buttons_lst = []

            for day_i in range(7):
                if start_day - day_of_week_number + day_i > days_in_month:
                    break

                if day_i < day_of_week_number:
                    row_buttons_lst.append(types.InlineKeyboardButton("\u200B", callback_data="empty"))
                else:
                    row_buttons_lst.append(types.InlineKeyboardButton(
                        str(start_day - day_of_week_number + day_i),
                        callback_data=f'departure_day_{str(start_day - day_of_week_number + day_i)}'))

            markup.row(*row_buttons_lst)
            row_buttons_lst = []

            for row_i in range(rows_count):
                current_day = start_day + days_in_first_row + (7 * row_i)
                for day_i in range(7):
                    if day_i + current_day <= days_in_month:
                        row_buttons_lst.append(types.InlineKeyboardButton(
                            str(day_i + current_day),
                            callback_data=f'departure_day_{str(day_i + current_day)}'))
                    else:
                        row_buttons_lst.append(types.InlineKeyboardButton("\u200B", callback_data="empty"))
                markup.row(*row_buttons_lst)
                row_buttons_lst = []

            return markup

        else:
            current_weekday = calendar.weekday(departure_year, departure_month, 1)  # номер дня недели первого числа
            current_day = 1

            # Добавляем дни месяца в ячейки
            while current_day <= days_in_month:
                row_buttons_lst = []
                for _ in range(current_weekday):
                    row_buttons_lst.append(types.InlineKeyboardButton("\u200B", callback_data="empty"))

                while current_weekday < 7 and current_day <= days_in_month:
                    row_buttons_lst.append(
                        types.InlineKeyboardButton(str(current_day), callback_data=f'departure_day_{str(current_day)}'))
                    current_day += 1
                    current_weekday += 1

                markup.row(*row_buttons_lst)
                current_weekday = 0

            return markup
