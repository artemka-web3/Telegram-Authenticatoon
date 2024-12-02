from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import TelegramProfile
import secrets

# Create your tests here.
class TelegramLoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('telegram_login')

    def test_telegram_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('bot_url', response.json())

class TelegramCallbackTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('telegram_callback')
        self.token = secrets.token_urlsafe(16)
        session = self.client.session
        session['tg_token'] = self.token
        session.save()

    def test_telegram_callback_invalid_token(self):
        response = self.client.get(self.url, {'token': 'invalid_token'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_telegram_callback_valid_token(self):
        telegram_id = 764315256
        username = 'sidnevart'
        response = self.client.get(self.url, {'token': self.token, 'telegram_id': telegram_id, 'username': username})
        print(response.content)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TelegramProfile.objects.filter(telegram_id=telegram_id).exists())

class VerifyOtpTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('verify_otp')
        self.user = get_user_model().objects.create_user(username='sidnevart', telegram_id=764315256)
        self.client.force_login(self.user)
        session = self.client.session
        session['otp_secret'] = 'JBSWY3DPEHPK3PXP'
        session['otp'] = '123456'
        session.save()

    def test_verify_otp_invalid(self):
        response = self.client.post(self.url, {'otp': '000000'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_verify_otp_valid(self):
        response = self.client.post(self.url, {'otp': '123456'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
