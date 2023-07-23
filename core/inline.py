from telebot.util import quick_markup

month_day = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

back_com = {"回到首頁": {"callback_data": "jump_entry"}}

def draw_entry():
    return quick_markup({
        "新增提醒事項": {"callback_data": "creat_remind"},
        "查詢提醒事項": {"callback_data": "search_remind"},
        "刪除提醒事項": {"callback_data": "delete_remind"}
    }, row_width=1)

def draw_day_ques():
    markup = {"上午":{"callback_data": "before"}, "下午":{"callback_data": "after"}}
    markup.update(back_com)
    markup = quick_markup(markup, row_width=2)
    return markup

def draw_hour(data):
    print(data)
    if data == "before":
        start = 0
    else:
        start = 12
    repeat = 0
    markup = {}

    while repeat < 12:
        markup.update({str(start + repeat): {"callback_data": str(start + repeat)}})
        repeat += 1
    markup = quick_markup(markup, row_width=6)
    return markup

def draw_min():
    i = 0
    markup = {}
    while i < 60:
        markup.update({str(i): {"callback_data": str(i)}})
        i += 15
    markup = quick_markup(markup, row_width=4)
    return markup

def draw_month():
    markup = {}
    i = 1
    while i <= 12:
        markup.update({str(i): {"callback_data": f"month_{i}"}})
        i += 1
    markup.update({'下一步': {"callback_data": 'next'}})
    markup.update({"回到首頁": {"callback_data": "jump_entry"}})
    markup = quick_markup(markup, row_width=6)
    return markup


def draw_ask_pattern():
    return quick_markup({
        "每年": {"callback_data": "yearly"},
        "每月": {"callback_data": "monthly"},
        "每周": {"callback_data": "weekly"},
        "每日": {"callback_data": "daily"},
        "回到首頁": {"callback_data": "jump_entry"}
        }, row_width=2)

def draw_confirm():
    return quick_markup({
        "是": {"callback_data": "yes"},
        "否": {"callback_data": "no"}
        }, row_width=2)