import secrets
import telebot
import pyotp
import logging
import os
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TelegramProfile
from telegram_auth.settings import TELEGRAM_BOT_USERNAME, TELEGRAM_BOT_TOKEN

logger = logging.getLogger(__name__)


bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


def index(request):
    user = request.user
    return render(request, 'index.html', {'user': user})

def telegram_login(request):
    unique_token = secrets.token_urlsafe(16)
    request.session['tg_token'] = unique_token
    bot_url = f"https://t.me/{TELEGRAM_BOT_USERNAME}?start={unique_token}"
    return JsonResponse({'bot_url': bot_url})

def telegram_callback(request):
    token = request.GET.get('token')
    telegram_id = request.GET.get('telegram_id')
    username = request.GET.get('username')

    if not token or token != request.session.get('tg_token'):
        return JsonResponse({'error': 'Invalid token'}, status=400)

    profile, created = TelegramProfile.objects.get_or_create(telegram_id=telegram_id)
    if created:
        profile.username = username
        profile.save()
        login(request, profile, backend='django.contrib.auth.backends.ModelBackend')
        logger.log(logging.INFO, f"New user created: {profile.username}")

    totp = pyotp.TOTP(pyotp.random_base32())
    otp = totp.now()
    request.session['otp_secret'] = totp.secret
    request.session['otp'] = otp

    bot.send_message(telegram_id, f"Ваш код: {otp}")

    return redirect('verify_otp')

@csrf_exempt
def verify_otp(request):
    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        otp_secret = request.session.get('otp_secret')
        otp_session = request.session.get('otp')

        if not otp_input or not otp_secret:
            logger.error("OTP or OTP secret not found in session")
            return JsonResponse({'error': 'Invalid OTP'}, status=400)
        totp = pyotp.TOTP(otp_secret)
        if totp.verify(otp_input) or otp_session == otp_input:
            if request.user.is_authenticated:
                return redirect('index')
            else:
                login(request, request.user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('index')
        else:
            logger.error("Invalid OTP provided")
            return JsonResponse({'error': 'Invalid OTP'}, status=400)

    return render(request, 'verify_otp.html')

