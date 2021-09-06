import os.path
from django.core.management.base import BaseCommand

from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, messagequeue as mq, InlineQueryHandler
)
from telegram.utils.request import Request

from src.settings import TOKEN_KEY
from tg.views import start, received_message

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        test_bot = TOKEN_KEY
        updater = Updater(token=test_bot, use_context=True, workers=32)
        dispatcher = updater.dispatcher

        # on different commands - answer in Telegram
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(MessageHandler(Filters.text, received_message))
        # dispatcher.add_handler(MessageHandler(Filters.contact, get_contact_value))
        # dispatcher.add_handler(CallbackQueryHandler(inline_query))

        updater.start_polling()
        updater.idle()
