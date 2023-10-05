from django.urls import path

from .views import *  # импорт функций представления

urlpatterns = [
    path('', ChatPage.as_view(), name='chat'),
    path('@<str:username>/', PersonalChatPage.as_view(), name='personal_chat'),
    path('=<int:chat_id>/', ChatPage.as_view(), name='group_chat'),
    path('new/', NewChat.as_view(), name='new_chat'),
]

