from django.db import models


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


class Chat(models.Model):
    name = models.CharField(max_length=30)
    personal = models.BooleanField(default=True)
    member = models.ManyToManyField('userface.CustomUser',
                                    related_name='member')
    admin = models.ForeignKey('userface.CustomUser',
                              on_delete=models.SET_NULL,
                              null=True,
                              related_name='admin')

    def __str__(self):
        return self.name
