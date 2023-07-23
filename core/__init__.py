import re
import logging
import threading
import json
import time

from telebot.async_telebot import AsyncTeleBot
from core.notify import new_notify, del_notify, show_notify
from core.inline import draw_entry, draw_month
from core.callback import handle_callback, reset, check_user_state, update_name

logging.basicConfig(level=logging.INFO)

with open("token.json", "r") as f:
    token = json.load(f)['token']
bot = AsyncTeleBot(token)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")


## TODO: 把這個改成純粹接收參數並創建任務
@bot.message_handler(commands=['remind'])
async def remind(message):
    reset(message.from_user.id)
    await bot.reply_to(message, "歡迎使用機器人", reply_markup = draw_entry() )

@bot.message_handler(commands=['delete'])
def delete(message):
    m1 = message.text.split()[1]
    del_notify(message.from_user.id, m1)

@bot.message_handler(commands=['delete'])
def delete(message):
    m1 = message.text.split()[1]
    del_notify(message.from_user.id, m1)

## TODO: 加上查詢任務的方法

@bot.message_handler(commands=['show'])
def show(message):
    bot.reply_to(message, "\n".join(show_notify(message.from_user.id)))


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    if check_user_state(chat_id=message.from_user.id, data="name_finish")['states'] == 'ask name':
        result = update_name(message.from_user.id,message.text, msg = message)
        print(result)
        await bot.reply_to(message, result['text'], reply_markup = result['reply_markup'])

@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    await bot.reply_to(message, message.text)

@bot.callback_query_handler(func=lambda cb: True)
async def call_back_dispach(call):
    result = handle_callback(call.data, call.message.chat.id)
    print(result)
    try :
        result['reply_markup']
        await bot.edit_message_text(result['text'], call.message.chat.id, call.message.message_id, reply_markup=result.get('reply_markup'))
    except KeyError:
        await bot.edit_message_text(result['text'], call.message.chat.id, call.message.message_id)
    except:
        await bot.edit_message_text("看起來你因為重複輸入過多次所以跳出來了", call.message.chat.id, call.message.message_id)