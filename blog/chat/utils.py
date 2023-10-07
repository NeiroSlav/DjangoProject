from django.db.models import Q

from userface.models import CustomUser
from .models import *
from .utils import *


def find_personal_chat(user1, user2) -> Chat:
    """поиск личного чата между юзерами"""
    chat_name = f'{user1}-to-{user2}'
    name_chat = f'{user2}-to-{user1}'
    chat = Chat.objects.filter(Q(name=chat_name) | Q(name=name_chat))

    if not chat:
        chat = [create_personal_chat(user1, user2)]

    return chat[0]


def create_personal_chat(user1, user2) -> Chat:
    """создание личного чата между юзерами"""
    new_chat = Chat(name=f'{user1}-to-{user2}')
    new_chat.save()
    add_user_to_chat(new_chat, [user1, user2])
    return new_chat


def add_user_to_chat(chat, username):
    """добавление юзера в чат (может принимать и список)"""
    if type(username) != list:
        username = [username]
    for u in username:
        user = CustomUser.objects.get(username=u)
        chat.member.set([user])
    chat.save()


def create_chat_list(writer):
    chat_list = Chat.objects.filter(member__username=writer)
    final_chat_list = []
    for elem in chat_list:
        try:
            final_chat_list.append({
                'title': elem.chatname_to_username(writer),
                'url': elem.get_absolute_url(writer)})
        except:
            final_chat_list.append({
                'title': elem.chatname_to_username(writer),
                'url': elem.get_absolute_url(writer)})

    return final_chat_list




main_menu = [
    {'title': 'все чаты', 'url': 'chat'},
    {'title': 'новый чат', 'url': 'new_chat'},
]

humble_menu = [
    {'title': 'инфо', 'url': 'about'},
    {'title': 'регистрация', 'url': 'register'}
]


def get_menu(request=None, humble=True):
    if request:
        return main_menu if request.user.is_authenticated \
            else humble_menu

    else:
        return humble_menu if humble \
            else main_menu


class DataMixin:
    """ОБЩИЕ ДАННЫЕ ДЛЯ НАСЛЕДУЕМЫХ КЛАССОВ"""

    @staticmethod
    def get_context(context={}):
        base = {
            'menu': get_menu(humble=False),
            'theme': 0
        }
        return base | context
