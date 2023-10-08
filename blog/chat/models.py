from django.db import models
from django.shortcuts import redirect
from django.urls import reverse


class Message(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey('Chat',
                             on_delete=models.CASCADE,
                             related_name='chat')
    user = models.ForeignKey('userface.CustomUser',
                             on_delete=models.SET_NULL,
                             null=True,
                             related_name='user')

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.text


class Chat(models.Model):
    name = models.CharField(max_length=30)
    personal = models.BooleanField(default=True)
    member = models.ManyToManyField('userface.CustomUser',
                                    related_name='member')
    admin = models.ForeignKey('userface.CustomUser',
                              on_delete=models.SET_NULL,
                              null=True,
                              related_name='admin')

    def get_title_and_url(self, writer) -> dict:
        if self.personal:
            title = self.chatname_to_username(writer)
            url = reverse('personal_chat', kwargs={'username': title})
        else:
            title = self.name
            url = reverse('group_chat', kwargs={'username': title})
        return {'title': title, 'url': url}

    def chatname_to_username(self, writer):
        chatname = self.name.replace('-to-', '')
        chatname = chatname.replace(writer, '')
        return chatname

    def __str__(self):
        return self.name
