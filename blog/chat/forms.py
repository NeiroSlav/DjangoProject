from django import forms

from .models import *


class NewChatForm(forms.ModelForm):
    class Meta:

        model = Chat
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-form'}),
        }


class NewMessageForm(forms.ModelForm):
    class Meta:

        model = Message
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'chat-input-form',
                                           'id': 'chat-input',
                                           'autocomplete': 'off'})
        }