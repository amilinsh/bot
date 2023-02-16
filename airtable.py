import os
from pyairtable import Table
from pyairtable.formulas import match

DB_TOKEN = os.environ['DB_TOKEN']
table = Table(DB_TOKEN, 'app5RAxelUKl2NZYo', 'Projects')

# Проверка на уникальность
def add_chat_id(chat_id, first_name, last_name, username):
  if len(table.all(formula=match({'chat_id': chat_id}))) == 0:
    table.create({"chat_id": chat_id,
                  'first_name': first_name,
                  'last_name': last_name,
                  'username': username})

# Получение списка чатов
def get_chats_id():
  chats_id = []
  chats = table.all()
  for chat in chats:
    chats_id.append(chat['fields']['chat_id'])
  return chats_id