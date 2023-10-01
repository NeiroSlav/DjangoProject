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





class Profile(DataMixin, View):
    """СТРАНИЧКА ПРОФИЛЯ ПОЛЬЗОВАТЕЛЯ"""

    def get(self, request, username=None):

        if username == None:
            username = request.user.username
            is_me = True
        else:
            is_me = False

        try:
            user = CustomUser.objects.get(username = username)
            username = user.username
            last_login = user.last_login
            user_id = user.id
            text = [
                f'ID пользователя: {user_id}',
                f'Последний раз заходил: {str(last_login).split()[0]}',
                f'Увлекательная информация, {username}',
            ]
        except:
            username = 'Пользователь не найден'
            text = ''

        context = {
            'menu': get_menu(request),
            'title': username,
            'text': text,
            'is_me': is_me,
        }

        return render(request, 'userface/profile.html', context=context)





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
