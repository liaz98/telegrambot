import os
from django.core.management.base import BaseCommand
import logging
from django.conf import settings
from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext, Filters, MessageHandler, Updater, CommandHandler
from telegram.utils.request import Request

from bottest.models import Message
from bottest.models import Profile


PORT = int(os.environ.get('PORT', '8443'))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)



def start(update, context):
    update.message.reply_text('Hi! you sent me /start. Lets start')


def help(update, context):
    update.message.reply_text('Help!')


def echo(update:Update, context:CallbackContext):
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    username = update.message.chat.username
    text = update.message.text
    p, _ = Profile.objects.get_or_create(
        external_id =chat_id,
        defaults={
            'name': username,
        }
    )

    Message(
        profile=p,
        text=text,
    ).save()

    reply_text = 'First name: {}\nLast name: {}\nUsername: @{}'.format(first_name, last_name, username)
    update.message.reply_text(text=reply_text,)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

class Command(BaseCommand):
    help = 'Telegram-bot'

    def handle(self, *args, **options):
        request = Request(connect_timeout=0.5, read_timeout=1)
        bot = Bot(request=request, token=settings.TOKEN, base_url=settings.PROXY_URL,)
        print(bot.get_me())
        updater = Updater(settings.TOKEN, use_context=True)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help))
        message_handler = MessageHandler(Filters.text, echo)
        dp.add_handler(message_handler)
        dp.add_error_handler(error)
        # updater.start_polling()
        updater.start_webhook(listen="0.0.0.0",
                              port=8443,
                              url_path=settings.TOKEN,
                              )
        updater.bot.setWebhook('https://azibonu.herokuapp.com/' + settings.TOKEN)
        updater.idle()
