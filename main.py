import pip

pip.main(['install', 'aiogram==2.25.1'])
pip.main(['install', 'apscheduler==3.10.0'])
pip.main(['install', 'pyairtable==1.4.0'])

import os
import logging
import apsched
import airtable

from aiogram import Bot, Dispatcher, executor, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

BOT_TOKEN = os.environ['BOT_TOKEN']

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# sheduler
date_start = datetime(2023, 2, 9, 17, 12, 0)
sheduler = AsyncIOScheduler(timezone="Europe/Moscow")

sheduler.add_job(apsched.send_message_first,
                 run_date=date_start + timedelta(hours=3, seconds=10),
                 kwargs={'bot': bot},
                 trigger="date")

sheduler.add_job(apsched.send_message_second,
                 run_date=date_start + timedelta(hours=3, seconds=20),
                 kwargs={'bot': bot},
                 trigger="date")

sheduler.add_job(apsched.send_message_third,
                 run_date=date_start + timedelta(hours=3, seconds=30),
                 kwargs={'bot': bot},
                 trigger="date")
sheduler.start()


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
  airtable.add_chat_id(message.chat.id, message.from_user.first_name,
                       message.from_user.last_name, message.from_user.username)

  # inline_buttons = [
  #   types.InlineKeyboardButton("Привет, Настюха!", callback_data="option_1"),
  #   types.InlineKeyboardButton("Option 2", callback_data="option_2"),
  #   types.InlineKeyboardButton("Option 3", callback_data="option_3")
  # ]
  reply_markup_hello = types.InlineKeyboardMarkup()
  reply_markup_hello.add(types.InlineKeyboardButton("Привет, Настюха!", callback_data="option_1"))
  await message.answer("Приветствую на моем бесплатном марафоне!",
                       reply_markup=reply_markup_hello)


@dp.callback_query_handler(lambda callback_query: True)
async def process_callback_data(callback_query: types.CallbackQuery):
  option = callback_query.data
  message = None

  if option == "option_1":
    message = "You selected option 1"
  elif option == "option_2":
    message = "You selected option 2"
  elif option == "option_3":
    message = "You selected option 3"
  else:
    message = "Invalid option selected"

  await bot.send_message(callback_query.from_user.id, text=message)


@dp.message_handler()
async def echo(message: types.Message):
  await bot.send_message(chat_id=message.chat.id, text='')


if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=True)
