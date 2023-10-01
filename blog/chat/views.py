from django.shortcuts import render, redirect
from django.views import View

from .models import *


class ChatCreate(View):
    """СОЗДАНИЕ НОВОГО ЧАТА"""

    def get(self, request):
        return redirect('main')


class ChatPage(View):
    """ВЫВОД СТРАНИЦЫ С ЧАТОМ И СПИСКОМ ЧАТОВ"""

    def get(self, request):
        return render(request, template_name='chat/chat.html')
