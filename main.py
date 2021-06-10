from telegram.ext import Updater, CommandHandler, dispatcher, MessageHandler, Filters, CallbackContext
from constants import TELEGRAM_TOKEN, REDIS_URL
import logging
import redis

updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
r = redis.from_url(REDIS_URL)
j = updater.job_queue
print(r)
db_keys = r.keys(pattern='*')

dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update, context):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.name
    r.set(user_name, user_id)

    message = 'Welcome to the bot'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def echo(update, context):
    context.bot.send_message(chat_id=update.effective.chat_id, text=update.message.text)

def main():
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)
    updater.start_polling()

if __name__ == '__main__':
    main()
