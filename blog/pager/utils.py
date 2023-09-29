from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from .models import *

menu = [{'title': 'статьи', 'url': 'list'},
        {'title': 'новая', 'url': 'new'},
        {'title': 'мои', 'url': 'mypage'},
        ]


class DataMixin:
    """ОБЩИЕ ДАННЫЕ ДЛЯ НАСЛЕДУЕМЫХ КЛАССОВ"""

    @staticmethod
    def get_context(context={}) -> dict:
        base = {
            'menu': menu,
            'theme': 0
        }
        return base | context


class LoginMixin(LoginRequiredMixin):
    """ПРОВЕРКА АВТОРИЗОВАННОГО ПОЛЬЗОВАТЕЛЯ"""

    login_url = 'login'
    redirect_field_name = "nonono"


# Декоратор методов get() для проверки авторства
def is_author(funk):
    def wrapper(self, request, page_id):
        page = Page.objects.get(id=page_id)
        if str(page.user) == request.user.username:
            return funk(self, request, page_id)
        else:
            return redirect('list')

    return wrapper
