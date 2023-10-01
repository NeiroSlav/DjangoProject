from django.db import models
from django.urls import reverse
from userface.models import CustomUser


class Page(models.Model):
    """МОДЕЛЬ ХРАНЕНИЯ СТАТЕЙ"""
    name = models.CharField(max_length=25)
    text = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('userface.CustomUser',
                             on_delete=models.SET_NULL,
                             null=True,
                             related_name='author')

    def __str__(self):
        return self.name

    # получение url-адреса text/page_id по объекту модели
    def get_absolute_url(self, prefix='text'):
        return reverse(prefix, kwargs={'page_id': self.id})

    # получение url-адреса del/page_id по объекту модели
    def get_absolute_url_del(self):
        return self.get_absolute_url('del')

    class Meta:
        ordering = ['-date']  # установка дефолтной сортировке по дате
