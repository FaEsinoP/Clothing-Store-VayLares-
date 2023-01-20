from django import template
from clothes.models import *

# Нужно при использовании функций-представлений, чтобы убрать дублирование кода

register = template.Library()


# @register.simple_tag()
# def get_categories(filter=None):
#     if not filter:
#         return Category.objects.all()
#     else:
#         return Category.objects.filter(pk=filter)


@register.inclusion_tag('clothes/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}
