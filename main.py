from datetime import datetime
from datetime import time
from telegram.ext import Updater, CommandHandler, dispatcher, MessageHandler, Filters, CallbackContext
from schedule_options import ScheduleOptionManager
import logging
import redis
import os

updater = Updater(token=os.environ['TELEGRAM_TOKEN'], use_context=True)
r = redis.from_url(os.environ['REDIS_URL'])
j = updater.job_queue
db_keys = r.keys(pattern='*')

dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def notify(context):
    schedule_option = context.job.context['schedule_option']
    user_id = context.job.context['user_id']
    context.bot.send_message(chat_id=user_id, text=schedule_option.notification_message())

def pay_for(update, context):
    user_id = update.message.from_user.id

    if len(context.args) == 0:
        context.bot.send_message(chat_id=user_id, text='You did\'t provide anything to subscribe for!')
        return
    schedule_option_name = context.args[0]
    schedule_option = ScheduleOptionManager.get_option(schedule_option_name)

    if not schedule_option:
        context.bot.send_message(chat_id=user_id, text='I don\'t know how to subscribe for that :(')
        return

    # j.run_once(notify, 10, context={'schedule_option': schedule_option, 'user_id': user_id })
    j.run_monthly(notify, when=time(hour=11, minute=0, second=0), day=15, context={'schedule_option': schedule_option, 'user_id': user_id})
    context.bot.send_message(chat_id=user_id, text=f'Your notification to pay for {schedule_option_name} is set.')

def start(update, context):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.name
    r.set(user_name, user_id)

    message = 'What do you want to pay for?'
    context.bot.send_message(chat_id=user_id, text=message)


def echo(update, context):
    print(db_keys)
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def main():
    start_handler = CommandHandler('start', start)
    schedule_notification_handler = CommandHandler('payFor', pay_for)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(schedule_notification_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
