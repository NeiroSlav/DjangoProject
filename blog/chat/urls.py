from django.urls import path

from .views import *  # импорт функций представления

urlpatterns = [
    path('<int:page_id>/', ChatPage.as_view(), name='chat'),
    path('new/', NewChat.as_view(), name='new_chat'),
    ]