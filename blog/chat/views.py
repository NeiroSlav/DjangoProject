from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from .forms import *
from .utils import *


class ChatPage(DataMixin, View):
    """ВЫВОД СТРАНИЦЫ БЕЗ ВЫБРАННОГО ЧАТА"""
    messages = ['asdf', '412341', 'qwerqw', '09897', 'zxcvzx']
    html = 'chat/chat.html'

    def get(self, request):
        self.context = self.get_context({'title': 'Чаты',
                                    'chat_name': 'Выберите чат'})

        return self.rendering(request,
                              context=self.context)

    def rendering(self, request, context):
        return render(request,
                      template_name=self.html,
                      context=context)


class PersonalChatPage(ChatPage):
    """ВЫВОД СТРАНИЦЫ С ПЕРСОНАЛЬНЫМ ЧАТОМ"""

    def get(self, request, username):
        """принимает логин пользователя"""
        self.form = NewMessageForm()
        self.assemble_chat(request, username)
        return self.rendering(request, self.context)

    def post(self, request, username):
        self.form = NewMessageForm(request.POST)
        self.assemble_chat(request, username)
        if self.form.is_valid():  # если форма валидна - сохраняет
            new_message = self.form.save(commit=False)
            new_message.chat = self.chat
            new_message.user = self.writer
            new_message.save()
            return redirect(reverse('personal_chat', kwargs={'username': username}))
        else:
            return self.rendering(request, self.context)

    def assemble_chat(self, request, username):
        self.writer = request.user.username
        self.writer = CustomUser.objects.get(username=self.writer)
        self.chat = find_personal_chat(self.writer, username)
        self.chat_name = f'> {username}'
        self.context = self.get_context({'title': 'Чаты',
                                         'chat_name': self.chat_name,
                                         'messages': self.messages,
                                         'form': self.form})


class NewChat(DataMixin, View):
    """СОЗДАНИЕ НОВОГО ЧАТА"""
    html_page = 'chat/new.html'

    def get(self, request):
        self.form = NewChatForm()
        return self.rendering(request)

    def post(self, request):
        self.form = NewChatForm(request.POST)
        if self.form.is_valid():  # если форма валидна - сохраняет
            user1 = request.user.username
            new_chat = self.form.save(commit=False)
            new_chat.admin = user1
            new_chat.save()
            add_user_to_chat(new_chat, user1)
            return redirect(reverse('chat', kwargs={'chat_name': new_chat.id}))

        else:  # если нет - отрисовывает вновь
            return self.rendering(request)

    def rendering(self, request):
        return render(request, self.html_page,
                      context=self.get_context({'title': 'Новый чат',
                                                'form': self.form
                                                }))