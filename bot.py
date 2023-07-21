from core import bot
from core.notify import scheduler

scheduler.start()
print("Log in")
bot.infinity_polling()