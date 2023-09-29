from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from .forms import *
from .utils import *


class ListPage(DataMixin, ListView):
    """ОТОБРАЖЕНИЕ СПИСКА СТАТЕЙ"""

    model = Page
    context_object_name = 'list'
    template_name = 'pager/list.html'
    extra_context = DataMixin.get_context({'title': 'Все статьи'})


class MyPage(DataMixin, View):
    """ОТОБРАЖЕНИЕ СПИСКА СТАТЕЙ"""

    def get(self, request):
        username = request.user.username
        pages = Page.objects.filter(user__username=username)

        context = self.get_context({
            'title': 'Все статьи',
            'list': pages,
            'delete_button': True,
        })
        return render(request, template_name='pager/list.html', context=context)


class TextPage(DataMixin, View):
    """ОТОБРАЖЕНИЕ СТАТЬИ"""

    def get(self, request, page_id):
        page = Page.objects.get(id=page_id)
        context = self.get_context({
            'id': page_id,
            'name': page.name,
            'text': page.text.split('\n'),
            'date': page.date,
            'edit_url': page.get_absolute_url('edit'),
            'author': page.user,
            'edit_access': (str(page.user) == request.user.username)
        })
        return render(request, "pager/text.html", context=context)


class NewPage(DataMixin, View):
    """СОЗДАНИЕ СТАТЬИ"""
    html_page = 'pager/new.html'

    # создание пустой формы, запрос на отрисовку
    def get(self, request):
        self.form = NewPageForm()
        return self.rendering(request)

    # проверяет валидность формы
    def post(self, request, page_id=None):
        self.form = NewPageForm(request.POST)
        if self.form.is_valid():  # если форма валидна - сохраняет
            self.saving(request, page_id)
            return redirect('list')
        else:  # если нет - отрисовывает вновь
            return self.rendering(request)

    # сохранение статьи
    def saving(self, request, page_id):
        new_page = self.form.save(commit=False)
        new_page.user = CustomUser.objects.get(username=request.user.username)
        new_page.save()
        print('Добавлена новая статья')

    # отрисовка страницы с формой, и контекстом, если он есть
    def rendering(self, request, context={}):
        return render(request, self.html_page,
                      context=self.get_context({'form': self.form} | context))


class EditPage(NewPage):
    """ИЗМЕНЕНИЕ СТАТЬИ"""
    html_page = 'pager/edit.html'

    # заполняется форма, запрос на отисовку
    @is_author
    def get(self, request, page_id):
        self.page = Page.objects.get(id=page_id)
        self.form = NewPageForm({'name': self.page.name,
                                 'text': self.page.text})
        return self.rendering(request, {'page': self.page})

    # сохренение статьи, переопределение saving()
    def saving(self, request, page_id):
        self.form = NewPageForm(request.POST)
        old_page = Page.objects.get(id=page_id)
        updated_page = NewPageForm(request.POST, instance=old_page)
        updated_page.save()
        print(f'Статья {page_id} обновлена')


class DeletePage(DataMixin, View):
    """УДАЛЕНИЕ СТАТЬИ"""

    # проверяется авторство
    @is_author
    def get(self, request, page_id):
        Page.objects.get(id=page_id).delete()
        print(f'Статья {page_id} удалена')
        return redirect('list')
