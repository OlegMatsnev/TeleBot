import telebot  # telebot

from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup  # States
from telebot import types
from my_calendar import Calendar

# States storage
from telebot.storage import StateMemoryStorage

# Starting from version 4.4.0+, we support storages.
# StateRedisStorage -> Redis-based storage.
# StatePickleStorage -> Pickle-based storage.
# For redis, you will need to install redis.
# Pass host, db, password, or anything else,
# if you need to change config for redis.
# Pickle requires path. Default path is in folder .state-saves.
# If you were using older version of pytba for pickle,
# you need to migrate from old pickle to new by using
# StatePickleStorage().convert_old_to_new()


# Now, you can pass storage to bot.
state_storage = StateMemoryStorage()  # you can init here another storage

bot = telebot.TeleBot("6438255358:AAGTFH3DZJS5uubvj7Y26w0UIEZXLATzzsg",
                      state_storage=state_storage)


# States group.
class MyStates(StatesGroup):
    month = State()
    day = State()
    rooms = State()
    city = State()
    main_commands = State()
    custom = State()
    low = State()
    high = State()
    history = State()
    # Each variable will return ClassName:variable_name
