import re
import json
import requests

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot.util import quick_markup
from core.spider import search_drug, search_side_effect
from core.inline import draw_entry, draw_month, draw_day_ques, draw_hour, draw_min, draw_confirm
from core.notify import new_notify, del_notify, show_notify, send_message, base_url

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
    'entry': ['creat_remind', "search_remind", "delete_remind", "jump_entry"],
    'noon': ['before', 'after', "jump_entry"],
    'hour': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'],
    'min': ['0', '15', '30', '45'],
    'ask name': ['name_finish'],
    "confirm name": ['confirm name', 'none', True],
    "confirm text": ['yes', 'no', 'none', 'confirm'],
    "finish": ['finish']
}

user_time_arg_temp = {}
"""
user_time_arg_temp = {
    chat_id: {
        hour: str, 
        min: str, 
        text: str, 
        drug: {state: bool, text: str}
    }
}
        
"""

def update_name(chat_id, text):
    user_state_dict.update({chat_id: 'confirm name'})
    print(user_time_arg_temp)
    user_time_arg_temp[chat_id].update({"text": text})
    return handle_callback("confirm name", chat_id)

def reset(chat_id):
    try:
        del user_state_dict[chat_id]
        user_state_dict.update({chat_id: 'entry'})
    except:
        pass

def check_user_state(data, chat_id: int, msg ='') -> dict:
    if user_state_dict.get(chat_id) is None:
        user_state_dict.update({chat_id:'entry'})
    print(user_state_dict.get(chat_id))
    if  data not in callback_data_state_dict.get(user_state_dict.get(chat_id)):
        if re.match(r".{6}[\d]{1,}號", data):
            print('Special')
            return {'states': user_state_dict[chat_id], 'description': "OK"}
        return {'states': 'error', 'description': '請按順序執行'}
    return {'states': user_state_dict[chat_id], 'description': "OK"}

def handle_callback(data: str, chat_id: int, msg = '') -> dict:
    try:
        user_state = check_user_state(data, chat_id)
        print(user_state)
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
                    user_time_arg_temp.update({chat_id: {}})
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
            user_time_arg_temp[chat_id].update({"hour": data})
            return {"text": f"分鐘\n目前選擇：{user_time_arg_temp[chat_id]['hour']}:", "reply_markup": draw_min()}
        
        elif user_state['states'] == 'min':
            print(user_time_arg_temp[chat_id])
            user_state_dict.update({chat_id: 'ask name'})
            user_time_arg_temp[chat_id].update({"min": data})
            send_message(chat_id, "請給我藥名")
            user_time_arg_temp[chat_id].update({"drug": {}})
            return {"text": f"目前選擇：{user_time_arg_temp[chat_id]['hour']}:{user_time_arg_temp[chat_id]['min']}"}
        
        elif user_state['states'] == 'confirm name':
            if data == 'confirm name':
                markup = []
                result = search_drug(user_time_arg_temp[chat_id]['text'])
                if len(result):
                    for i in result:
                        markup.append([InlineKeyboardButton(text=i['name'],callback_data=i['id'])])
                else:
                    markup.append([InlineKeyboardButton(text='找不到',callback_data='none')])
                markup = InlineKeyboardMarkup(markup)
                print(result)
                return {"text": "請確認藥物", "reply_markup": markup}
            
            else:
                user_state_dict.update({chat_id: 'confirm text'})
                if data == 'none':
                    return handle_callback("no", chat_id)
                result = search_side_effect(data)
                print(user_time_arg_temp[chat_id]['drug'])
                user_time_arg_temp[chat_id]['drug'].update({'state': True})
                user_time_arg_temp[chat_id]['drug'].update({'text': result})
                return {'text': f'請確認 {result}', "reply_markup": draw_confirm()}

        
        elif user_state['states'] == 'confirm text':

            if data == 'yes':
                user_state_dict.update({chat_id: 'finish'})
                user_time_arg_temp[chat_id]['drug'].update({'state': True})
                return handle_callback("finish", chat_id)
            
            elif data == 'no':
                print("no")
                user_time_arg_temp[chat_id]['drug'].update({'state': False})
                user_state_dict.update({chat_id: 'finish'})
                return handle_callback("finish", chat_id)
            
            elif data == 'confirm':

                text = f"請確認 {user_time_arg_temp[chat_id]['hour']}:{user_time_arg_temp[chat_id]['min']} 提醒 {user_time_arg_temp[chat_id]['text']}"
                print(text)
                return {"text" : text, "reply_markup": draw_confirm()}


            else:
                raise BaseException("Unknow")
            
        elif user_state['states'] == 'recheck':
            user_state_dict.update({chat_id: 'finish'})
            return{"就這樣了"}

        elif user_state['states'] == 'ask name':
            return{"就這樣了"}

        elif user_state['states'] == 'finish':
            print("GOOD")
            user_state_dict.update({chat_id: 'entry'})
            time_arg = f"hour = {user_time_arg_temp[chat_id]['hour']}, minute = {user_time_arg_temp[chat_id]['min']}"
            id = f"{user_time_arg_temp[chat_id]['hour']}--{user_time_arg_temp[chat_id]['min']}--{user_time_arg_temp[chat_id]['text']}"
            print(time_arg)
            print(id)

            if user_time_arg_temp[chat_id]['drug']['state']:

                print("GOOD")
                text = user_time_arg_temp[chat_id]['text'] + user_time_arg_temp[chat_id]["drug"]["text"] + "\n"
                print(text)
                print(f'''new_notify(chat_id = {chat_id}, 
                text = "{text}",
                time = "cron", id = "{id}", time_arg = "{time_arg}" )''')
                exec(f'''new_notify(chat_id = {chat_id}, 
                text = """{user_time_arg_temp[chat_id]['text'] + user_time_arg_temp[chat_id]["drug"]["text"]}""",
                time = "cron", id = "{id}", time_arg = "{time_arg}" )''')

            else:
                exec(f'new_notify(chat_id = {chat_id}, text = "{user_time_arg_temp[chat_id]["text"]}",  time = "cron", id = "{id}", time_arg="{time_arg}")')

            time = f"{user_time_arg_temp[chat_id]['hour']}:{user_time_arg_temp[chat_id]['min']}"
            del user_time_arg_temp[chat_id]
            print(user_time_arg_temp)
            return {'text': f"設定 {time}"}
        
        elif data == "name_finish":
            user_state_dict.update({chat_id: 'confirm'})
            return handle_callback(data='confirm', chat_id=chat_id)

        else:
            raise BaseException(f"沒有找到與 {data} 相符的處理方式")

    except BaseException as e:
        print("BUG!!!")
        print("Here is something you might use")
        print(e)
        print(f"data: {data}, user_time_arg_temp: {user_time_arg_temp}, user_state_dict: {user_state_dict}, user_state: {user_state}")
        return {"text": f"ERROR, Please Check Log. {e}"} 
    except:
        print("BUG!!!")
        print("Here is something you might use")
        print(f"data: {data}, user_time_arg_temp: {user_time_arg_temp}, user_state_dict: {user_state_dict}, user_state: {user_state}")
        return {"text": "ERROR, Please Check Log"} 