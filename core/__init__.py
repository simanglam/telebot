import logging
import telebot
import requests
import schedule
import threading
import json
import time

bot = telebot.TeleBot("6307331536:AAG0dCgb5iiDKkkWE-IZ6pScdDRGOpbWSp0")
base_url = "https://api.telegram.org/bot6307331536:AAG0dCgb5iiDKkkWE-IZ6pScdDRGOpbWSp0/"


def run_continuously(interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run

# Start the background thread
stop_run_continuously = run_continuously()
def remind():
    requests.post(f'{base_url}sendMessange', {"chat_id": 2020724351, "text": "He"})

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")

@bot.message_handler(commands=['remind'])
def send_welcome(message):
    arg = message.text.split()[1:]
    schedule.every().second.do(remind)

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)

stop_run_continuously = run_continuously()
