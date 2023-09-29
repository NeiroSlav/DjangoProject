from django import forms
from django.core.exceptions import ValidationError

from .models import *


# class NewPageForm(forms.Form):
#     name = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class': 'input-form'}),
#                            label='Название:')
#     text = forms.CharField(widget=forms.Textarea({'cols': 50, 'rows': 15}),
#                            label='Текст статьи:')
#
class NewPageForm(forms.ModelForm):
    class Meta:

        model = Page
        fields = ['name', 'text']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-form'}),
            'text': forms.Textarea(attrs={'cols': 50, 'rows': 13})
        }

    def clean_name(self):
        name = self.cleaned_data['name']

        if name == 'Богдан чурка':
            raise ValidationError('Сам ты чурка, пёс поганый')

        return name
