from django.contrib.auth.mixins import LoginRequiredMixin

main_menu = [
    {'title': 'статьи', 'url': 'list'},
    {'title': 'чаты', 'url': 'main'},
    {'title': 'инфо', 'url': 'about'}
]

humble_menu = [
    {'title': 'инфо', 'url': 'about'},
    {'title': 'регистрация', 'url': 'register'}
]

def get_menu(request=None, humble=True):
    if request:
        return main_menu if request.user.is_authenticated \
            else humble_menu

    else:
        return humble_menu if humble \
            else main_menu


class DataMixin:
    '''ОБЩИЕ ДАННЫЕ ДЛЯ НАСЛЕДУЕМЫХ КЛАССОВ'''

    @staticmethod
    def get_context(context={}):
        base = {
            'menu': get_menu(humble=False),
            'theme': 0
        }
        return base | context


class LoginMixin(LoginRequiredMixin):
    login_url = 'login'
    redirect_field_name = "forbidden"
