from aiogram import Bot, Dispatcher

from settings import config

bot = Bot(config.bot_token.get_secret_value())
dp = Dispatcher(bot)
