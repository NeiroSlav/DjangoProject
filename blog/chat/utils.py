from userface.models import CustomUser
from .models import *
from .utils import *


def find_personal_chat(user1, user2) -> Chat:
    """поиск личного чата между юзерами"""
    chat = Chat.objects.filter(member__username=user1)
    chat = chat.filter(member__username=user2)
    chat = chat.filter(personal=True)

    if not chat:
        chat = [create_personal_chat(user1, user2)]

    return chat[0]


def create_personal_chat(user1, user2) -> Chat:
    """создание личного чата между юзерами"""
    new_chat = Chat(name=f'{user1}-to-{user2}')
    new_chat.save()
    add_user_to_chat(new_chat, [user1, user2])

    return new_chat


def add_user_to_chat(chat, usernames):
    """добавление юзера в чат (может принимать и список)"""
    if type(usernames) != list:
        usernames = [usernames]
    users = []
    for i in range(len(usernames)):
        user = CustomUser.objects.get(username=usernames[i])
        users.append(user)

    chat.member.set(users)
    chat.save()


def create_chat_list(writer, selected_chat=None):
    """создание списка сайтов для отображения на панели слева"""
    chat_list = Chat.objects.filter(member__username=writer)
    final_chat_list = []
    for elem in chat_list:
        chat_bar = elem.get_title_and_url(writer)
        if elem == selected_chat:
            chat_bar['selected'] = True
        final_chat_list.append(chat_bar)

    return final_chat_list

def messages_to_json(messages):
    json_messages = []
    for m in messages:
        json_messages.append({'text': str(m.text), 'user': str(m.user)})
    return json_messages



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
