import requests
import logging
import json

from apscheduler.schedulers.background import BackgroundScheduler


with open("token.json", "r") as f:
    token = json.load(f)['token']
scheduler = BackgroundScheduler()


user_notify_dict = {}
dummy = []

base_url = f"https://api.telegram.org/bot{token}/"

def remind(chat_id, text):
    r = requests.post(f'{base_url}sendMessage', {"chat_id": chat_id, "text": text})
    logging.info(f"Status Code: {r}, INFO : {r.text}")


def new_notify(chat_id, text, time, time_arg=""):
    if user_notify_dict.get(chat_id) is None:
        user_notify_dict.update({chat_id: []})
    user_notify_dict[chat_id].append(text)
    exec(f"""scheduler.add_job(
remind,  '{time}', {time_arg}, args=[chat_id, text], id="{chat_id}--{text}"
)
""")

def del_notify(chat_id, text):
    if user_notify_dict.get(chat_id) is None:
        user_notify_dict.update({chat_id: []})
    scheduler.remove_job(f"{chat_id}--{text}")
    user_notify_dict[chat_id].remove(text)

def show_notify(chat_id):
    if user_notify_dict.get(chat_id) is None or len(user_notify_dict[chat_id]) == 0:
        return ["No You Have none"]
    
    return user_notify_dict[chat_id]
