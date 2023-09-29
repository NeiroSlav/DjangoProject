from django.db import models


class Message(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    chat = models.ForeignKey('Chat',
                             on_delete=models.CASCADE)
    user = models.ForeignKey('userface.CustomUser',
                             on_delete=models.SET_NULL,
                             null=True)

    class Meta:
        ordering = ['date']


class Chat(models.Model):
    name = models.CharField(max_length=30)
    members = models.ManyToOneRel
