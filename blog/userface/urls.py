from django.urls import path
from userface.views import *

urlpatterns = [
    path('', MainPage.as_view(), name='main'),
    path('about/', AboutPage.as_view(), name='about'),

    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),

    path('settings/', Settings.as_view(), name='settings'),
    path('theme/', Theme.as_view(), name='theme'),
]
