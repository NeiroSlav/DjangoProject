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
        return self.rendering(request,
                              context=self.get_context())

    def rendering(self, request, context):
        return render(request,
                      template_name=self.html,
                      context=context)


class PersonalChatPage(ChatPage):
    """ВЫВОД СТРАНИЦЫ С ПЕРСОНАЛЬНЫМ ЧАТОМ"""

    def get(self, request, username):
        """принимает логин пользователя"""

        writer = request.user.username
        chat = find_personal_chat(writer, username)
        chat_name = f'> {username}'
        context = self.get_context({'title': 'Чаты',
                                    'chat_name': chat_name,
                                    'messages': self.messages})

        return self.rendering(request, context)





























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