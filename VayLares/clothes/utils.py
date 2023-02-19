from django.db.models import Count, Q
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

        subcats = Subcategory.objects.all()

        user_menu = menu.copy()

        if not self.request.user.is_superuser:
            user_menu.pop(2)

        context['menu'] = user_menu

        search_request = self.request.GET.get('search', '').title()
        search_result = Clothes.objects.filter(Q(title__icontains=search_request) |
                                               Q(brand__brand_name__icontains=search_request) |
                                               Q(category__category_name__icontains=search_request) |
                                               Q(subcategory__subcategory_name__icontains=search_request),
                                               is_published=True).select_related('category', 'brand')
        if search_request:
            context['search_request'] = search_request
            context['search_count'] = search_result.count()
            context['goods'] = search_result

        context['cats'] = cats
        context['subcats'] = subcats

        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        if 'subcat_selected' not in context:
            context['subcat_selected'] = 0
        if 'gender_selected' not in context:
            context['gender_selected'] = 0
        return context
