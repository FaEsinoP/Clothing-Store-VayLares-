from django.db.models import Count
from django.core.cache import cache
from .models import *

menu = [{'title': "Для мужчин", 'url_name': 'man'},
        {'title': "Для женщин", 'url_name': 'woman'},
        {'title': "Добавить позицию", 'url_name': 'add'}
        ]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        cats = cache.get('cats')
        if not cats:
            cats = Category.objects.annotate(Count('clothes'))
            cache.set('cats', cats, 60)

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(2)

        context['menu'] = user_menu

        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
