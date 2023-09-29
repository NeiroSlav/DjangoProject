from django.urls import path

from .views import *  # импорт функций представления

urlpatterns = [
    path('list/<int:page_id>/', TextPage.as_view(), name='text'),
    path('list/', ListPage.as_view(), name='list'),
    path('mypage/', MyPage.as_view(), name='mypage'),

    path('new/', NewPage.as_view(), name='new'),
    path('edit/<int:page_id>/', EditPage.as_view(), name='edit'),
    path('del/<int:page_id>/', DeletePage.as_view(), name='del'),

    # path('about/', About.as_view(), name='about'),
    # path('theme/', Theme.as_view(), name='theme'),
    # path('login/', Login.as_view(), name='login'),
]
