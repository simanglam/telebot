from telebot.util import quick_markup

month_day = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def draw_entry():
    return quick_markup({
        "新增提醒事項": {"callback_data": "creat_remind"},
        "查詢提醒事項": {"callback_data": "search_remind"},
        "刪除提醒事項": {"callback_data": "delete_remind"}
    }, row_width=1)

def draw_day(month: int):
    markup = {}
    i = 1
    while i <= month_day[month - 1] or i % 7 != 0:
        if i <= month[month]:
            markup.update({str(i): {"callback_data": f"day_{i}"}})
        i += 1

    markup = quick_markup(markup, row_width=7)
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