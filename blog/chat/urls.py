from django.urls import path

from .views import *  # импорт функций представления

urlpatterns = [
    path('', ChatPage.as_view(), name='chat'),
    path('new/', NewChat.as_view(), name='new_chat'),
    path('redirect/<str:username>/', PersonalChat.as_view(), name='personal_chat'),
    path('<str:chat_id>/', ChatPage.as_view(), name='chat'),
    ]
