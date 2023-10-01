from django import forms

from .models import *


class NewChatForm(forms.ModelForm):
    class Meta:

        model = Chat
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-form'}),
        }
