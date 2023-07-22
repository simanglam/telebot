import re
import json

from telebot.util import quick_markup
from core.inline import draw_entry, draw_month, draw_day_ques, draw_hour, draw_min
from core.notify import new_notify, del_notify, show_notify, send_message

wait_notify = []
wait_name = []

user_state_dict = {}

state_dict = {
    "entry": 0,
    "noon": 2,
    "hour": 3,
    "min": 4,
    "ask notify": 5,
    "ask name": 6,
    "confirm": 7,
    "recheck": 8,
    "finish": 9
}

callback_data_state_dict = {
    'entry': ['creat_remind'],
    'noon': ['before', 'after'],
    'hour': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'],
    'min': ['0', '15', '30', '55'],
    'confirm': ['before', 'after'],
    'recheck': ['before', 'after'],
}

user_time_arg_temp = {}
"""
user_time_arg_temp = {chat_id: [{hour: str, min: str, text: str, drug: optional}, {}]}
"""

def is_wait_name(chat_id):
    if chat_id in wait_name:
        return True
    return False

def is_wait_notify(chat_id):
    if chat_id in wait_notify:
        return True
    return False
    

def reset(chat_id):
    try:
        del user_state_dict[chat_id]
        user_state_dict.update({chat_id: 'entry'})
    except:
        pass

def check_user_state(data, chat_id: int) -> dict:
            print(user_time_arg_temp)
            if user_state_dict.get(chat_id) is None:
                user_state_dict.update({chat_id:'entry'})
            if callback_data_state_dict.get(data) != user_state_dict[chat_id] and callback_data_state_dict.get(data) != None :
                return {'states': 'error', 'description': '請按順序執行'}
            return {'states': user_state_dict[chat_id], 'description': "OK"}

def handle_callback(data: str, chat_id: int) -> dict:
    try:
        user_state = check_user_state(data, chat_id)
        if user_state['states'] == 'error':
            raise BaseException(f"你沒有按照順序")
        
        if data == "jump_entry":
            print('jump back')
            print(user_state_dict)
            user_state_dict.pop(chat_id)
            print(user_state_dict)
            try:
                del user_time_arg_temp[chat_id]
            finally:
                return {'text': 'main page', 'reply_markup': draw_entry()}

        elif user_state['states'] == 'entry':

            if data.startswith("creat"):
                if user_time_arg_temp.get(chat_id) is None:
                    user_time_arg_temp.update({chat_id: []})
                if len(user_time_arg_temp[chat_id]) == 0:
                    user_time_arg_temp[chat_id].append({})
                user_state_dict.update({chat_id: 'noon'})
                return {"text": "請問提醒時間", "reply_markup": draw_day_ques()}

            elif data.startswith("search"):
                result = show_notify(chat_id)
                print(result)
                if result.get("reply_markup"):
                    return {"text": result['text'], 'reply_markup': quick_markup(result.get('reply_markup'))}
                return {"text": result['text']}

            elif data.startswith("delete"):
                user_state = check_user_state(data, chat_id)
                if user_state['states'] == 'error':
                    return {"text": f"{user_state['states']}. Error massage: {user_state['description']}"}
                else:
                    return{"text":f"{user_state['states']}"}
                
            else:
                raise BaseException("非有效 Entry 選項")
            
        elif user_state['states'] == 'noon':
            user_state_dict.update({chat_id: 'hour'})
            return {"text": "小時\n目前選擇：", "reply_markup": draw_hour(data)}
        
        elif user_state['states'] == 'hour':
            print(user_time_arg_temp[chat_id])
            user_state_dict.update({chat_id: 'min'})
            user_time_arg_temp[chat_id][-1].update({"hour": data})
            return {"text": f"分鐘\n目前選擇：{user_time_arg_temp[chat_id][-1]['hour']}:", "reply_markup": draw_min()}
        
        elif user_state['states'] == 'min':
            print(user_time_arg_temp[chat_id])
            user_state_dict.update({chat_id: 'ask name'})
            user_time_arg_temp[chat_id][-1].update({"min": data})
            send_message(chat_id, "請給我藥名")
            return {"text": f"目前選擇：{user_time_arg_temp[chat_id][-1]['hour']}:{user_time_arg_temp[chat_id][-1]['min']}"}
        
        elif user_state['states'] == 'ask name':
            print(user_time_arg_temp[chat_id])
            # user_state_dict.update({chat_id: 'ask name'})
        
        else:
            raise BaseException(f"沒有找到與 {data} 相符的處理方式")

            
    except BaseException as e:
        print("BUG!!!")
        print("Here is something you might use")
        print(e)
        return {"text": "ERROR, Please Check Log", 'reply_markup': draw_hour(data)} 
    except:
        print("BUG!!!")
        print("Here is something you might use")
        print(data)
        return {"text": "ERROR, Please Check Log", 'reply_markup': draw_hour(data)} 