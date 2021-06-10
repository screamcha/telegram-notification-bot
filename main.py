from telegram.ext import Updater, CommandHandler, dispatcher, MessageHandler, Filters, CallbackContext
import logging
import redis
import os

updater = Updater(token=os.environ['TELEGRAM_TOKEN'], use_context=True)
print(os.environ['TELEGRAM_TOKEN'])
r = redis.from_url(os.environ['REDIS_URL'])
j = updater.job_queue
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
    print('start working')
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)
    updater.start_polling()

if __name__ == '__main__':
    main()
