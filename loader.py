from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from settings import config

bot = Bot(config.bot_token.get_secret_value())


storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)


