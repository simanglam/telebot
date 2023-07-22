from core import bot
from core.notify import scheduler
import asyncio

scheduler.start()
print("Log in")
asyncio.run(bot.infinity_polling())

print("AA")
scheduler.remove_all_jobs()