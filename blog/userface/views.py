from django.shortcuts import render
from django.views import View

from pager.models import Page
from .reg_views import *
from .utils import *


class MainPage(View):
    """ОТОБРАЖЕНИЕ ГЛАВНОЙ СТРАНИЦЫ"""
    title = 'Главная'
    search = 'main_page'

    def get(self, request):
        try:
            text = Page.objects.get(name=self.search).text
        except:
            text = f'Добавьте статью с именем {self.search}'

        context = {
            'menu': get_menu(request),
            'title': self.title,
            'text': text.split('\n')
        }
        return render(request, 'userface/main.html', context=context)


class AboutPage(MainPage):
    """ОТОБРАЖЕНИЕ СТРАНИЦЫ <<О САЙТЕ>>"""
    title = 'О сайте'
    search = 'about_page'


class Theme(LoginMixin, View):
    """CМЕНА ТЕМЫ ОФОРМЛЕНИЯ"""

    def get(self, request):
        username = request.user.username
        user = CustomUser.objects.get(username=username)
        # print('тема перед изменением:', user.theme)
        user.theme = not user.theme
        user.save()
        # print('тема после изменением:', user.theme)
        return redirect('settings')


class Settings(LoginMixin, DataMixin, View):
    """ПОЛЬЗОВАТЕЛЬСКИЕ НАСТРОЙКИ"""

    def get(self, request):
        username = request.user.username
        # theme = CustomUser.objects.get(username=username).theme
        context = self.get_context({
            'title': 'Настройки',
            'theme': 0,
        })
        # print(context['theme'])
        return render(request, 'userface/settings.html', context)
