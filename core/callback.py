import re
import json

from telebot.util import quick_markup
from core.inline import draw_entry, draw_month, draw_ask_pattern
from core.notify import new_notify, del_notify, show_notify

user_state_dict = {}

state_dict = {
    "entry": 0,
    "ask pattern": 1,
    "yearly": 2,
    "monthly": 2,
    "weekly": 2,
    "daily": 2,
    "ask notify": 3
}

callback_data_state_dict = {
    'creat_remind': 'entry',
    'year': 'yearly',
    'month': 'monthly',
    'week': 'weekly',
    'day': 'daily',
}

user_time_arg_temp = {}

def reset(chat_id):
    try:
        del user_state_dict[chat_id]
        user_state_dict.update({chat_id: 'entry'})
    except:
        pass

def handle_callback(data: str, chat_id: int) -> dict:
    try:
        def check_user_state(data, chat_id: int) -> dict:
            if user_state_dict.get(chat_id) is None:
                user_state_dict.update({chat_id:'entry'})
            if callback_data_state_dict.get(data) != user_state_dict[chat_id] and callback_data_state_dict.get(data) != None :
                return {'states': 'error', 'description': '請按順序執行'}
            return {'states': user_state_dict[chat_id], 'description': "OK"}

        user_state = check_user_state(data, chat_id)
        if user_state['states'] == 'error':
            return {"text": f"{user_state['states']}. Error massage: {user_state['description']}"}
        
        if data == "jump_entry":
            print('jump back')
            print(user_state_dict)
            user_state_dict.pop(chat_id)
            print(user_state_dict)
            try:
                del user_time_arg_temp[chat_id]
            finally:
                return {'text': 'main page', 'reply_markup': draw_entry()}

        if user_state['states'] == 'entry':

            if data.startswith("creat"):
                user_state_dict.update({chat_id: 'ask pattern'})
                user_time_arg_temp.update({chat_id: {}})
                return {"text": "請問你的提醒頻率是", 'reply_markup': draw_ask_pattern()}

            if data.startswith("search"):
                result = show_notify(chat_id)
                print(result)
                if result.get("reply_markup"):
                    return {"text": result['text'], 'reply_markup': quick_markup(result.get('reply_markup'))}
                return {"text": result['text']}

            if data.startswith("delete"):
                user_state = check_user_state(data, chat_id)
                if user_state['states'] == 'error':
                    return {"text": f"{user_state['states']}. Error massage: {user_state['description']}"}
                else:
                    return{"text":f"{user_state['states']}"}
                
        if user_state['states'] == 'ask pattern':
            if data == ('monthly'):
                if user_time_arg_temp.get(chat_id) is None:
                    user_time_arg_temp.update({chat_id: {}})
                if user_time_arg_temp[chat_id].get('monthly') is None:
                    user_time_arg_temp[chat_id].update({'monthly': []})
                user_state_dict.update({chat_id: 'monthly'})
                return {'text': f'請選擇月份\n已選擇月份:\{"".join(user_time_arg_temp[chat_id]["monthly"])}', 'reply_markup': draw_month()}
            
        if user_state['states'] == 'monthly':
            print(data)
            if data == "next":
                user_state_dict.update({chat_id: 'ask notify'})
                return {"text": "So far So good"}
            print(user_time_arg_temp[chat_id]["monthly"])
            if data.strip()[6:] in user_time_arg_temp[chat_id]["monthly"] and len(user_time_arg_temp[chat_id]["monthly"]) != 0:
                return {'text': f'你重複輸入了\n請選擇月份\n已選擇月份: {"".join(user_time_arg_temp[chat_id]["monthly"])}', 'reply_markup': draw_month()}
            user_time_arg_temp[chat_id]['monthly'].append(''.join(data.strip()[6:]))
            return {'text': f'請選擇月份\n已選擇月份: {" ".join(user_time_arg_temp[chat_id]["monthly"])}', 'reply_markup': draw_month()}

            
        
    except:
        print("BUG!!!")
        return {"text": "ERROR, Please Check Log", 'reply_markup': draw_month()} 