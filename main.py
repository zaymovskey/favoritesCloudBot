from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
import os

load_dotenv()

bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(text="Тест")


if __name__ == "__main__":
    executor.start_polling(dp)
