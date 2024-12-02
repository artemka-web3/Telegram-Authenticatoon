from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('telegram-login/', views.telegram_login, name='telegram_login'),
    path('telegram-callback/', views.telegram_callback, name='telegram_callback'),

    path('verify-otp/', views.verify_otp, name='verify_otp'),
]
