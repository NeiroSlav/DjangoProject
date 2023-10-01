from django.views import View
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import *
from .utils import *


class RegisterUser(DataMixin, CreateView):
    """РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ"""
    form_class = RegisterUserForm
    template_name = 'userface/register.html'
    success_url = reverse_lazy('main')
    extra_context = DataMixin.get_context({
        'menu': get_menu(),
        'title': 'Регистрация'})

    def form_valid(self, form):
        print('Пользователь зарегистрировался')
        user = form.save()
        login(self.request, user)
        return redirect('main')


class LoginUser(DataMixin, LoginView):
    """ВХОД В АККАУНТ"""
    form_class = LoginUserForm
    template_name = 'userface/login.html'
    extra_context = DataMixin.get_context({
        'menu': get_menu(),
        'title': 'Авторизация'})

    def get_success_url(self):
        print('Пользователь авторизовался')
        return reverse_lazy('main')


def logout_user(request):
    """ВЫХОД ИЗ АККАУНТА"""
    logout(request)
    return redirect('login')

