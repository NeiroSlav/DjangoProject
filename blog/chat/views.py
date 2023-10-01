from django.shortcuts import render, redirect
from django.views import View
from userface.models import CustomUser

from .models import *
from .forms import *
from .utils import *


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
            user2 = 'jjake'

            user1 = CustomUser.objects.get(username=user1)
            user2 = CustomUser.objects.get(username=user2)

            new_chat = self.form.save(commit=False)
            new_chat.save()
            new_chat.member.set([user1,user2])
            new_chat.save()

            print('Добавлен новый чат')
            return redirect('main')
        else:  # если нет - отрисовывает вновь
            return self.rendering(request)

    def rendering(self, request):
        return render(request, self.html_page,
                      context=self.get_context({'title': 'Новый чат',
                                                'form': self.form
                                                }))


class ChatPage(View):
    """ВЫВОД СТРАНИЦЫ С ЧАТОМ И СПИСКОМ ЧАТОВ"""

    def get(self, request):
        return render(request, template_name='chat/chat.html')
