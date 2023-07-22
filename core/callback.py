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
        user_state_dict.update({chat_id: {'states': 'entry', 'description': "OK"}})
    except:
        pass

def handle_callback(data: str, chat_id: int) -> dict:
    try:
        def check_user_state(data, chat_id: int) -> dict:
            if user_state_dict.get(chat_id) is None:
                user_state_dict.update({chat_id: {'states': 'entry', 'description': "OK"}})
            if callback_data_state_dict.get(data) != user_state_dict[chat_id]['states'] and callback_data_state_dict.get(data) != None :
                return {'states': 'error', 'description': '請按順序執行'}
            return {'states': user_state_dict[chat_id]['states'], 'description': "OK"}

        user_state = check_user_state(data, chat_id)
        if user_state['states'] == 'error':
            return {"text": f"{user_state['states']}. Error massage: {user_state['description']}"}

        if user_state['states'] == 'entry':

            if data.startswith("creat"):
                user_state_dict[chat_id].update({'states': 'ask pattern'})
                user_time_arg_temp.update({chat_id: []})
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
            if data.startswith('month'):
                user_state_dict[chat_id].update({'states': 'monthly'})
                user_time_arg_temp[chat_id].append('month = ')
                return {'text': f'請選擇月份\n已選擇月份:', 'reply_markup': draw_month()}
            
        if user_state['states'] == 'monthly':
            if data == "next":
                user_state_dict[chat_id].update({'states': 'ask notify'})
                return 
            user_time_arg_temp[chat_id].append("".join(data.split()[1:]))
            print(user_time_arg_temp)
            return {'text': f'請選擇月份\n已選擇月份: {" ".join(user_time_arg_temp[chat_id][1:])}', 'reply_markup': draw_month()}

        if data == "jump_entry":
            
            user_state_dict.update({chat_id: {'states': 'entry'}})
            try:
                del user_time_arg_temp[chat_id]
            except:
                pass
            print(handle_callback(data, chat_id))
            return handle_callback(data, chat_id)
        
    except:
        return {"text": "ERROR, Please Check Log"}