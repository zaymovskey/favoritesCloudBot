from aiogram import Bot, Dispatcher, executor, types
from settings import config

bot = Bot(config.bot_token.get_secret_value())
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(text="Тест")


if __name__ == "__main__":
    executor.start_polling(dp)
