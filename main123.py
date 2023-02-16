import os
from background import keep_alive

import pip
pip.main(['install', 'aiogram'])
pip.main(['install', 'apscheduler'])

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import apsched
from datetime import datetime, timedelta

TOKEN = os.environ['TOKEN']

datetime_object = datetime.now()
date_start = datetime(2023, 2, 9, 17, 12, 0)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

sheduler = AsyncIOScheduler(timezone="Europe/Moscow")

sheduler.add_job(apsched.send_message_first,
                 trigger="date",
                 run_date=datetime.now() + timedelta(hours=3, seconds=10),
                 kwargs={'bot': bot})

sheduler.add_job(apsched.send_message_second,
                 trigger="date",
                 run_date=datetime.now() + timedelta(hours=3, seconds=15),
                 kwargs={'bot': bot})

sheduler.add_job(apsched.send_message_third,
                 run_date=datetime.now() + timedelta(hours=3, seconds=20),
                 kwargs={'bot': bot},
                 trigger="date")

sheduler.start()

hello_message = """Привет!👋
в пятницу в 10:00 МСК ты получишь первый шаблон
"""

def add_chat_id(chat_id):
  try:
    chat_id = str(chat_id)
    with open("chats.txt", "r+") as file:
        chats_id = file.read()
        if len(chats_id) == 0:
            file.write(chat_id)
        else:
            if chat_id not in chats_id:
                file.write(";" + chat_id)
  except Exception as e:
      print(str(e))

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
  add_chat_id(message.chat.id)
  await message.reply(hello_message)

keep_alive()
if __name__ == '__main__':
    executor.start_polling(dp)