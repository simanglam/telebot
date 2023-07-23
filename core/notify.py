import requests
import logging
import json

from apscheduler.schedulers.background import BackgroundScheduler


with open("token.json", "r") as f:
    token = json.load(f)['token']
scheduler = BackgroundScheduler()


user_notify_dict = {}

'''
demo user_notify_dict
user_notify_dict = {chat_id:[] }
'''

base_url = f"https://api.telegram.org/bot{token}/"

def send_message(chat_id, text):
    r = requests.post(f'{base_url}sendMessage', {"chat_id": chat_id, "text": text})
    logging.info(f"Status Code: {r}, INFO : {r.text}")


def new_notify(chat_id, text, time, id, time_arg=""):
    if user_notify_dict.get(chat_id) is None:
        user_notify_dict.update({chat_id: []})
    user_notify_dict[chat_id].append(text)
    exec(f"""scheduler.add_job(
send_message,  '{time}', {time_arg}, args=[chat_id, text], id="{id}"
)
""")

def del_notify(chat_id, text):
    if user_notify_dict.get(chat_id) is None:
        user_notify_dict.update({chat_id: []})
    scheduler.remove_job(f"{chat_id}--{text}")
    user_notify_dict[chat_id].remove(text)

def show_notify(chat_id) -> dict:
    if user_notify_dict.get(chat_id) is None or len(user_notify_dict[chat_id]) == 0:
        return {'text':"No You Have none", 'reply_markup': {"回到首頁": {"callback_data": "jump_entry"}}}
    result = {'text': '以下是你現有的提醒', 'reply_markup':{}}
    for i in user_notify_dict[chat_id]:
        result['reply_markup'].update({f"{i}": {}})
    return result
