import schedule
import time

async def notify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    notify_arr.update({"chat_id": update.effective_chat.id, 'content': []})