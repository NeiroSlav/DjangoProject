from django.shortcuts import render
from django.views import View

from userface.utils import LoginMixin
from .forms import *
from .utils import *


class ChatPage(LoginMixin, DataMixin, View):
    """ВЫВОД СТРАНИЦЫ БЕЗ ВЫБРАННОГО ЧАТА"""
    chat_names = ['aboba', 'kuzima', 'osadok', 'zhmich']
    chat_names = chat_names * 5

    def get(self, request):
        self.context = self.get_context({'title': 'Чаты', 'chat_name': '< Выберите чат',
                                         'all_chats': create_chat_list(request.user.username)})
        return self.rendering(request, context=self.context)

    def rendering(self, request, context):
        return render(request, 'chat/chat.html', context)


class PersonalChatPage(ChatPage):
    """ВЫВОД СТРАНИЦЫ С ЛИЧНЫМ ЧАТОМ"""

    def get(self, request, username):  # принимает логин пользователя

        if not CustomUser.objects.filter(username=username) or (request.user.username == username):
            return redirect('chat')

        self.form = NewMessageForm()
        self.assemble_chat(request, username)
        return self.rendering(request, self.context)

    def post(self, request, username):  # при отправке сообщения сохраняет его
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

    def assemble_chat(self, request, username):  # метод для сборки нужных данных
        self.writer_name = request.user.username
        self.writer = CustomUser.objects.get(username=self.writer_name)
        self.chat = find_personal_chat(self.writer, username)
        self.chat_name = f'{username}'
        self.all_chats = create_chat_list(self.writer_name, self.chat)
        self.messages = Message.objects.filter(chat__name=self.chat.name)
        self.context = self.get_context({'title': 'Чаты',
                                         'all_chats': self.all_chats,
                                         'chat_name': self.chat_name,
                                         'messages': self.messages,
                                         'writer': self.writer,
                                         'form': self.form}, )


class NewChat(LoginMixin, DataMixin, View):
    """СОЗДАНИЕ НОВОГО ЧАТА"""
    html_page = 'chat/new.html'

    def get(self, request):
        self.form = NewChatForm()
        return self.rendering(request)

    def post(self, request):
        self.form = NewChatForm(request.POST)
        if self.form.is_valid():  # если форма валидна - сохраняет
            user = CustomUser.objects.get(username=request.user.username)
            new_chat = self.form.save(commit=False)
            new_chat.admin = user
            new_chat.save()
            add_user_to_chat(new_chat, user)
            return redirect(reverse('chat', kwargs={'chat_name': new_chat.id}))

        else:  # если нет - отрисовывает вновь
            return self.rendering(request)

    def rendering(self, request):
        context = self.get_context({'title': 'Новый чат',
                                    'form': self.form})
        return render(request, self.html_page, context)
