import time
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from userface.models import CustomUser

from .models import *
from .forms import *
from .utils import *


def add_user_to_chat(chat, username):
    """добавление юзера в чат (может принимать и список)"""
    if type(username) != list:
        username = [username]
    for u in username:
        user = CustomUser.objects.get(username=u)
        chat.member.set([user])
    chat.save()
    print('добавил юзера в чат')


def find_personal_chat(user1, user2):
    chat_name = f'{user1}-to-{user2}'
    name_chat = f'{user2}-to-{user1}'
    return Chat.objects.filter(Q(name=chat_name) | Q(name=name_chat))


class NewChat(DataMixin, View):
    """СОЗДАНИЕ НОВОГО ЧАТА"""
    html_page = 'chat/new.html'

    def get(self, request):
        self.form = NewChatForm()
        return self.rendering(request)

    def post(self, request):
        print('Процесс добавнеия нового чата')
        self.form = NewChatForm(request.POST)
        if self.form.is_valid():  # если форма валидна - сохраняет

            user1 = request.user.username

            new_chat = self.form.save(commit=False)
            new_chat.admin = user1
            new_chat.save()
            add_user_to_chat(new_chat, user1)

            print('Добавлен новый чат')
            return redirect(reverse('chat', kwargs={'chat_name': new_chat.id}))
        else:  # если нет - отрисовывает вновь
            return self.rendering(request)

    def rendering(self, request):
        return render(request, self.html_page,
                      context=self.get_context({'title': 'Новый чат',
                                                'form': self.form
                                                }))


class PersonalChat(View):
    """ОБРАБОТКА КНОПКИ <<НАПИСАТЬ>>"""

    def get(self, request, username):
        writer = request.user.username

        chat = find_personal_chat(writer, username)

        if not chat:  # если такого чата нет, то создаёт, добавляет юзеров, и открывает его
            new_chat = Chat(name=f'{writer}-to-{username}')
            new_chat.save()
            add_user_to_chat(new_chat, [writer, username])

        return redirect(reverse('chat', kwargs={'chat_id': f'@{username}'}))


class ChatPage(DataMixin, View):
    """ВЫВОД СТРАНИЦЫ С ЧАТОМ И СПИСКОМ ЧАТОВ"""

    def get(self, request, chat_id=None):
        """chat_id может быть @логином собеседника или id чата"""

        if chat_id[0] == '@':
            writer = request.user.username
            username = chat_id.replace('@', '')
            chat = find_personal_chat(writer, username)
            chat_name = f'> {username}'
        else:
            chat = Chat.objects.get(id=chat_id)
            chat_name = chat.name


        messages = ['asdf', '412341', 'qwerqw', '09897', 'zxcvzx']

        context = self.get_context({'title': 'Чаты',
                                    'chat_id': chat_id,
                                    'name': chat_name,
                                    'messages': messages})

        return render(request,
                      template_name='chat/chat.html',
                      context=context)
