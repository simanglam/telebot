import logging
import telebot
import threading
import json
import time
from core.notify import new_notify, del_notify, show_notify

logging.basicConfig(level=logging.INFO)

with open("token.json", "r") as f:
    token = json.load(f)['token']
bot = telebot.TeleBot(token)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")


## TODO: 把這個改成純粹接收參數並創建任務
@bot.message_handler(commands=['remind'])
def remind(message):
    m1 = message.text.split()[1]
    m2 = message.text.split()[2]
    new_notify(message.from_user.id, m1, 'interval', m2)

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
def echo_message(message):
    bot.reply_to(message, message.text)

