from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.
class TelegramProfile(AbstractUser):
    telegram_id = models.IntegerField()
    username = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.username
