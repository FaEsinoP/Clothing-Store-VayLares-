from django.http import HttpResponse
from django.shortcuts import render

from clothes.models import Clothes, Category

menu = [{'title': "Для мужчин", 'url_name': 'man'},
        {'title': "Для женщин", 'url_name': 'woman'},
        {'title': "Добавить позицию", 'url_name': 'add'},
        {'title': "Войти", 'url_name': 'login'},
        {'title': "О сайте", 'url_name': 'about'},
        ]


def index(request):
    goods = Clothes.objects.all()
    cats = Category.objects.all()
    context = {
        'goods': goods,
        'cats': cats,
        'menu': menu,
        'title': 'Главная страница',
        'cat_selected': 0,
    }

    return render(request, 'clothes/index.html', context=context)


def for_man(request):
    goods = Clothes.objects.filter(gender='All')
    return render(request, 'clothes/man.html', {'goods': goods, 'title': 'Для мужчин', 'menu': menu})


def for_woman(request):
    return render(request, 'clothes/woman.html', {'title': 'Для женщин', 'menu': menu})


def about(request):
    return render(request, 'clothes/about.html', {'title': 'О сайте', 'menu': menu})


def login(request):
    return HttpResponse("Авторизаtion")


def add(request):
    return HttpResponse("Добавление позиции")


def show_category(request, category_id):
    goods = Clothes.objects.filter(category=category_id)
    cats = Category.objects.all()
    context = {
        'goods': goods,
        'cats': cats,
        'menu': menu,
        'title': 'Главная страница',
        'cat_selected': category_id,
    }

    return render(request, 'clothes/index.html', context=context)
