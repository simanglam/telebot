import logging
import telebot
import requests
from apscheduler.schedulers.background import BackgroundScheduler
import threading
import json
import time

logging.basicConfig(level=logging.INFO)

scheduler = BackgroundScheduler()

bot = telebot.TeleBot("6307331536:AAG0dCgb5iiDKkkWE-IZ6pScdDRGOpbWSp0")
base_url = "https://api.telegram.org/bot6307331536:AAG0dCgb5iiDKkkWE-IZ6pScdDRGOpbWSp0/"

def remind(chat_id, text):
    r = requests.post(f'{base_url}sendMessage', {"chat_id": chat_id, "text": text})
    logging.info(f"Status Code: {r}, INFO : {r.text}")


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")

@bot.message_handler(commands=['remind'])
def send_welcome(message):
    print(message.from_user.id)
    type(message.from_user.id)
    arg = message.text.split()[1:]
    scheduler.add_job(
        remind,  'interval', args=[message.from_user.id, arg], seconds = 0.5, id=f"{message.from_user}-{arg}"
        )

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


