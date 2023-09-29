from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

from .models import *


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-form'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-form'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-form'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-form'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-form'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'password')
