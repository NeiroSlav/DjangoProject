import copy

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


def get_default_settings():
    default_settings = {
        'theme': 0,
        'font': 0
    }
    return copy.deepcopy(default_settings)


class CustomUser(AbstractUser):
    """МОДЕЛЬ ХРАНЕНИЯ ПОЛЬЗОВАТЕЛЕЙ"""
    settings = models.JSONField('settings',
                                default=get_default_settings)

    def __str__(self):
        return self.username

    def get_absolute_url(self, prefix='personal_chat'):
        return reverse(prefix, kwargs={'username': self.username})
