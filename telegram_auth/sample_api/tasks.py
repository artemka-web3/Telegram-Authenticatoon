from celery import shared_task
from .models import TelegramProfile
import telebot

bot = telebot.TeleBot("8066960076:AAEtuYOTnZi4DFHXeC2UdL2VruBewckfgVw")

@shared_task
def send_telegram_message(telegram_id, message):
    bot.send_message(chat_id=telegram_id, text=message)
