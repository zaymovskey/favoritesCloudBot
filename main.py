from aiogram import Bot, Dispatcher, executor, types
from settings import config

bot = Bot(config.bot_token.get_secret_value())
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    print(message)
    await message.answer(text="Привет")


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(text="Тест")


if __name__ == "__main__":
    print("The bot is running!")
    executor.start_polling(dp)
