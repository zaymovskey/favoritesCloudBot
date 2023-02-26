from aiogram import executor
from handlers import dp


if __name__ == "__main__":
    print("The bot is running!")
    executor.start_polling(dp)
